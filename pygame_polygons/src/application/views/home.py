import pygame
from pygame.math import Vector2
from typing import Optional
from ..gui import GuiPanel, GuiButton
from .view_manager import ViewManager

from ..services import ShapeController


class ViewHome(ViewManager):
    SHAPE_VERTEX_MIN: int = 3
    SHAPE_VERTEX_MAX: int = 100

    def __init__(self, *args):
        super().__init__(*args)

        self.shape_new_vertex: int = 3
        self.current_figure: tuple = ()
        self.current_figure_center: Optional[int] = None
        self.current_figure_wheel: Optional[bool] = False
        self.current_figure_drag: bool = False

        # Shapes
        self.polygons: list[list[Vector2]] = []
        self.stars: list[list[Vector2]] = []

    def register_mouse_action(self, hooked: bool):
        """Register user mouse actions.
        If hooked is True, that means that an object is currenly performing an action
        (for example, mouse is on top of a draggable component)
        :param hooked: bool
        :return:
        """
        if not hooked:
            self.mouse_reset_drag_and_pointer()
            return

        # mouse wheel
        self.current_figure_wheel = self.app.event_listener.event_get_mouse_wheel()
        # mouse drag
        if not self.current_figure_wheel:
            if self.app.event_listener.is_mouse_button_pressed_event():  # mouse press and drag
                self.mouse_init_drag()
            elif self.app.event_listener.is_mouse_button_released_event():  # mouse release
                self.mouse_reset_drag()

    def mouse_reset_drag_and_pointer(self) -> None:
        """Resets Mouse drag event actions and set default mouse pointer"""
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.mouse_reset_drag()

    def mouse_reset_drag(self) -> None:
        """Reset mouse drag event actions"""
        self.current_figure = ()
        self.current_figure_center = None
        self.current_figure_drag = False

    def mouse_init_drag(self) -> None:
        """Init mouse drag event action"""
        self.current_figure_drag = True

    def is_current_object_used(self, index_i: int, index_y: int) -> bool:
        return (
                self.current_figure_drag
                and self.current_figure
                and self.current_figure[0] == index_i
                and self.current_figure[1] == index_y

        )

    def is_near_poly_centroid(self, poly_index: int, mouse_current: tuple, centroid: Vector2) -> bool:
        """Detects if the mouse is close enough to the center and 'hook' it if it is.
        If the center was previously tackled by the user than the 'sensibility' (area / margin)
        is bigger, similar of method: _get_point_detection_margin

        :param poly_index:
        :param mouse_current:
        :param centroid:
        :return:
        """
        # first we check the center, if is grabbed then it has priority over vertices
        margin = 3
        if self.current_figure_center == poly_index:
            # draggin multiplier
            # fast user (like me) that move the mouse quick will notice that, so we need to
            # increase the mouse area otherwise as soon as the mouse moves too fast, the vertex
            # won't follow the mouse pointer and stops following it!
            margin *= 25

        if ShapeController.shape_vertex_is_near_mouse_pointer(mouse_current, centroid,
                                                              margin):  # give some pixel of margin
            self.current_figure = ()
            self.current_figure_center = poly_index
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            return True

        return False

    def highlight_polygon_vertex(self, matches_previous_polygon: Optional[Vector2], matches: list[Vector2]) -> bool:

        # when matches_previous_polygon then user is still on the previous polygon - area / functionality
        if matches_previous_polygon:
            self.current_figure = (int(matches_previous_polygon.x), int(matches_previous_polygon.y))
            self.current_figure_center = None
            self.vertex_dot_focus(matches_previous_polygon)
            return True
        # Then a new vertex is approached
        if matches:
            match = matches[0]  # todo: should get the vertex with closest to mouse and not the first found
            self.vertex_dot_focus(match)
            self.current_figure = (match[0], match[1])
            self.current_figure_center = None

            return True

        return False

    def _render_polygons(self, mouse_current: tuple) -> bool:
        """Render the polygons
        Returns whether or not a polygon is 'hooked' by a user event, for instance a mouse hover
        mouse drag, mouse rotation etc..

        :param mouse_current: tuple x,y mouse coordinates
        :return: bool True if a polygon is currently withing a user event , False otherwise
        """

        hooked = False
        for poly_index, poly in enumerate(self.polygons):
            centroid = ShapeController.shape_get_center(poly)
            self.polygon_draw(poly, centroid)


            matches: list[Vector2] = []
            matches_previous_polygon: Optional[Vector2] = None
            # First, wee need to collect all vertex and check if there is a match. That's because
            # we need to know whether the user is still draggin the same vertex around. Else if we have a match
            # the new match found is the new vertex.
            for vertex_index, vertex in enumerate(poly):

                self.write_vertex_coords(vertex)

                margin, current = self._get_point_detection_margin(poly_index, vertex_index)

                if ShapeController.shape_vertex_is_near_mouse_pointer(mouse_current, vertex,
                                                                      margin):  # give some pixel of margin
                    matches.append(Vector2(poly_index, vertex_index))
                    if current:  # if the current object then we can just exit the loop
                        matches_previous_polygon = Vector2(poly_index, vertex_index)
                        break

            # Check if the user is near the center of the polygon
            is_it = self.is_near_poly_centroid(poly_index, mouse_current, centroid)
            if is_it:
                hooked = True
                continue
            hooked = self.highlight_polygon_vertex(matches_previous_polygon, matches)

        return hooked

    def view_logic(self):
        # inputs
        # shape controlls

        components_gui = pygame.sprite.Group()
        # panel
        panel_left_size = Vector2(250, self.app.win_height)
        panel_left = GuiPanel(Vector2(0, 0), panel_left_size, self.app, self.app.background, None, {})
        components_gui.add(panel_left)

        # button
        def action(event: dict):
            if 'MOUSE_LEFT' not in event:
                return
            # Make a new draw
            half_w = self.app.win_width / 2
            half_h = self.app.win_height / 2
            polygon = ShapeController.make_polygon(self.shape_new_vertex, 150, (half_w, half_h))
            self.polygons.append(polygon)

            # reset the new vertex counter
            self.shape_new_vertex = self.SHAPE_VERTEX_MIN

        btn_new_shape = GuiButton("New Shape", Vector2((panel_left_size.x / 2), 50), None,
                                  self.app, panel_left.image, panel_left, {})
        btn_new_shape.add_event_listener("click", action)
        # add child to panel
        panel_left.children_add(btn_new_shape)

        def vertex_add(event: dict):
            if 'MOUSE_LEFT' not in event:
                return

            self.shape_new_vertex += 1
            if self.shape_new_vertex > self.SHAPE_VERTEX_MAX:
                self.shape_new_vertex = self.SHAPE_VERTEX_MAX

        def vertex_remove(event: dict):
            if 'MOUSE_LEFT' not in event:
                return

            self.shape_new_vertex -= 1
            if self.shape_new_vertex < self.SHAPE_VERTEX_MIN:
                self.shape_new_vertex = self.SHAPE_VERTEX_MIN

        # add vertex buttons
        btn_vertex_remove = GuiButton("-", Vector2((panel_left_size.x / 2 - 20), 150), Vector2(25, 25),
                                      self.app, panel_left.image, panel_left, {})
        btn_vertex_remove.add_event_listener("click", vertex_remove)
        # add child to panel
        panel_left.children_add(btn_vertex_remove)

        btn_vertex_add = GuiButton("+", Vector2((panel_left_size.x / 2 + 20), 150), Vector2(25, 25),
                                   self.app, panel_left.image, panel_left, {})
        btn_vertex_add.add_event_listener("click", vertex_add)
        # add child to panel
        panel_left.children_add(btn_vertex_add)

        def screen_clear(event: dict):
            if 'MOUSE_LEFT' not in event:
                return
            self.polygons.clear()
            self.stars.clear()

        # screen clear
        btn_screen_clear = GuiButton("Clear", Vector2((panel_left_size.x / 2), 350), None,
                                     self.app, panel_left.image, panel_left, {})
        btn_screen_clear.add_event_listener("click", screen_clear)
        # add child to panel
        panel_left.children_add(btn_screen_clear)

        # btn_star

        def make_star(event: dict):
            if 'MOUSE_LEFT' not in event:
                return
            half_w = self.app.win_width / 4 + (len(self.stars) * len(self.stars))
            if len(self.stars) % 2 == 0:
                half_h = self.app.win_height / 2 - ((len(self.stars) * len(self.stars)) - 50)
            else:
                half_h = self.app.win_height / 2 + ((len(self.stars) * len(self.stars)) - 50)

            self.stars.append(ShapeController.make_polygon(3, 150, (half_w, half_h)))

        def remove_star(event: dict):
            if 'MOUSE_LEFT' not in event:
                return
            if self.stars:
                self.stars.pop()

        btn_star = GuiButton("Make star", Vector2((panel_left_size.x / 2), 450), None,
                             self.app, panel_left.image, panel_left, {})
        btn_star.add_event_listener("click", make_star)

        btn_star_remove = GuiButton("Remove star", Vector2((panel_left_size.x / 2), 500), None,
                                    self.app, panel_left.image, panel_left, {})
        btn_star_remove.add_event_listener("click", remove_star)

        # add child to panel
        panel_left.children_add(btn_star)
        panel_left.children_add(btn_star_remove)

        # button button_navigate_about
        def view_about(event: dict):
            if 'MOUSE_LEFT' not in event:
                return
            self.app.view_current = "about"
            self.close_view = True

        button_navigate_about = GuiButton("About", Vector2((panel_left_size.x / 2), self.app.win_height - 50), None,
                                          self.app, panel_left.image, panel_left, {
                                              'background_color': pygame.Color("grey"),
                                              'border_color': pygame.Color("grey")
                                          })
        button_navigate_about.add_event_listener("click", view_about)
        # add child to panel
        panel_left.children_add(button_navigate_about)

        def _update():

            # Update Gui Components
            components_gui.draw(self.app.background)
            components_gui.update()

            # Render Text
            about_text1 = f"Vertex = {self.shape_new_vertex}"
            font_img = self.app.font.render(about_text1, True, (255, 255, 255))
            panel_left.image.blit(font_img, Vector2((panel_left_size.x / 2 - (font_img.get_rect().width / 2)), 100))

            # make draws
            mouse_current = pygame.mouse.get_pos()
            mouse_x = mouse_current[0]
            mouse_y = mouse_current[1]

            # ---------------------------------------------------------
            # SHAPES
            # ---------------------------------------------------------
            hooked: bool = self._render_polygons(mouse_current)
            # -------------------------------------------------------- #

            # ---------------------------------------------------------
            #   KEYBOARD / MOUSE CONTROL
            # ---------------------------------------------------------
            self.register_mouse_action(hooked)

            # .............. drag center ............... #
            if self.current_figure_center is not None and self.current_figure_drag:
                ShapeController().move_polygon(self.polygons, self.current_figure_center, mouse_current)

            # .............. drag vertex ............... #
            elif self.current_figure and self.current_figure_drag:
                self.polygons[int(self.current_figure[0])][int(self.current_figure[1])] = Vector2(mouse_x, mouse_y)

            # .............. central rotation ............... #
            if self.current_figure_center is not None and self.current_figure_wheel:
                direction: str = "clockwise"
                if self.current_figure_wheel == "WHEEL_DOWN":
                    direction = "counter_clockwise"

                ShapeController().rotate_polygon(self.polygons, self.current_figure_center, direction)

            # ---------------------------------------------------------
            #  STARTS
            # ---------------------------------------------------------
            ShapeController().draw_stars(self.app.background, self.stars)

        return _update

    # -----------------
    # Utility functions
    # -----------------

    def vertex_dot_focus(self, polygon: Vector2) -> None:
        """Focus a Vertex, make it in a red dot

        :param polygon:
        :return:
        """
        try:
            vertex = self.polygons[int(polygon.x)][int(polygon.y)]
        except IndexError as err:
            print(str(err))
            return
        pygame.draw.circle(self.app.background, (255, 0, 0),  # draw red dot around vertex
                           Vector2(vertex[0], vertex[1]), 5)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

    def polygon_draw(self, poly: list, centroid: Vector2):
        """ Draws a polygon and its center dot (centroid / barycenter)

        :param poly:
        :param centroid:
        :return:
        """
        pygame.draw.circle(self.app.background, (79, 0, 153),  # draw red dot around vertex
                           Vector2(centroid.x, centroid.y), 5)
        self.write_vertex_coords(centroid)
        pygame.draw.polygon(self.app.background, pygame.Color("green"), poly, width=2)

    def write_vertex_coords(self, vertex: Vector2):
        """Write the coordinates of a particualr vertex"""
        # write vertex coordinates into the vertex
        about_text1 = f"{round(vertex.x, 2)}-{round(vertex.y, 2)}"
        font_img = self.app.font_small.render(about_text1, True, (255, 255, 255))
        self.app.background.blit(font_img,
                                 Vector2(vertex.x + 5, vertex.y + 5))


    def _get_point_detection_margin(self, poly_index: int, vertex_index: int) -> tuple:
        """Detects the margin by witch a point is sensible to a mouse detection when is near
        A object that in the previus frame, and still now is been used (basically under some user funciont or event like
        mouse dragging) then the area is target, therefore the 'margin' too.

        :param poly_index:
        :param vertex_index:
        :return:
        """
        margin = 3
        current = False
        if self.is_current_object_used(poly_index, vertex_index):
            # draggin multiplier
            # fast user (like me) that move the mouse quick will notice that, so we need to
            # increase the mouse area otherwise as soon as the mouse moves too fast, the vertex
            # won't follow the mouse pointer and stops following it!
            margin *= 55
            current = True
        return margin, current

