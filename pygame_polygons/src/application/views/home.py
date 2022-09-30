import pygame
from pygame.math import Vector2
from typing import Optional
from ..gui import GuiPanel, GuiButton
from .view_manager import ViewManager

from .components import PolygonSettingWindow

from ..services import ShapeController
from ..shapes import Polygon


class ViewHome(ViewManager):
    SHAPE_VERTEX_MIN: int = 3
    SHAPE_VERTEX_MAX: int = 100

    VIEW_MODES: tuple = ('polygons', 'polygon_selecting', 'polygon_selected')

    def __init__(self, *args):
        super().__init__(*args)

        # Shapes
        self.polygons: list[Polygon] = []
        self.stars: list[Polygon] = []

        self.shape_new_vertex: int = 3
        self.current_figure: tuple = ()
        self.current_figure_center: Optional[int] = None
        self.current_selected_polygon: Optional[int] = None
        self.mode: str = self.VIEW_MODES[0]

        # ------------- GUI components ------------- #
        self.gui_polygon_settings: PolygonSettingWindow = PolygonSettingWindow(self.app, self)

        # ------------- INPUTS ------------- #

        # mouse
        self.current_figure_wheel: bool = False
        self.current_figure_drag: bool = False

        # keyboard
        self.event_ctrl_l: Optional[str] = None

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

    def register_keyboard_action(self, hooked: bool):

        if not hooked:
            ...
        if self.event_ctrl_l == 'PRESSED':
            is_ctrl_l_released = self.app.event_listener.is_ctrl_left_released_event()
            self.event_ctrl_l = is_ctrl_l_released and 'RELEASED' or 'PRESSED'
        else:
            is_ctrl_l_pressed = self.app.event_listener.is_ctrl_left_pressed_event()
            self.event_ctrl_l = is_ctrl_l_pressed and 'PRESSED' or None

        if self.event_ctrl_l == 'RELEASED' and self.current_selected_polygon is None:
            self.keyboard_reset_selected_polygon()

        elif self.event_ctrl_l == 'PRESSED' and self.mode == 'polygons':
            # Initalize the 'selection' mode
            self.mode = self.VIEW_MODES[1]

    def keyboard_reset_selected_polygon(self):
        self.current_selected_polygon = None
        self.mode = self.VIEW_MODES[0]

    def mouse_reset_drag_and_pointer(self) -> None:
        """Resets Mouse drag event actions and set default mouse pointer"""
        if not self.app.event_listener.element_hovered:
            if self.mode == 'polygon_selecting':
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
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
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_CROSSHAIR:
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
            self.current_figure = (int(match[0]), int(match[1]))
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

        hooked: Optional[str] = None
        for poly_index, poly in enumerate(self.polygons):
            is_hooked = self._render_polygon(poly_index, mouse_current, hooked, is_selected=False)
            if is_hooked and not hooked:
                hooked = is_hooked

            if hooked == "HOOKED_CENTER":
                # Check the mode.
                if self.mode == 'polygon_selecting':
                    self.current_selected_polygon = poly_index
                    self.mode = self.VIEW_MODES[2]
                    break  # break execution of loop immediatelly
        return bool(hooked)

    def _render_polygon(self, poly_index: int, mouse_current: tuple, hooked: Optional[str], is_selected: bool = False) -> \
    Optional[str]:
        polygon: Polygon = self.get_selected_polygon(poly_index)
        if not polygon and is_selected:
            self.keyboard_reset_selected_polygon()
            return None

        polygon.draw()
        centroid: Vector2 = polygon.centroid

        matches: list[Vector2] = []
        # First, wee need to collect all vertex and check if there is a match. That's because
        # we need to know whether the user is still draggin the same vertex around. Else if we have a match
        # the new match found is the new vertex.
        matches_previous_polygon: Optional[Vector2] = self._render_polygon_vertices(polygon, matches, poly_index,
                                                                                    mouse_current)
        # Check if the user is near the center of the polygon
        if not hooked:
            is_it = self.is_near_poly_centroid(poly_index, mouse_current, centroid)
            if is_it:
                return "HOOKED_CENTER"

        hooked = self.highlight_polygon_vertex(matches_previous_polygon, matches)
        return hooked and "HOOKED_VERTEX" or None

    def _render_polygon_vertices(self, polygon: Polygon, matches: list[Vector2], poly_index: int, mouse_current: tuple):
        vertices: list[Vector2] = polygon.vertices
        for vertex_index, vertex in enumerate(vertices):
            polygon.write_vertex_coords(vertex)

            margin, current = self._get_point_detection_margin(poly_index, vertex_index)
            if ShapeController.shape_vertex_is_near_mouse_pointer(mouse_current, vertex,
                                                                  margin):  # give some pixel of margin
                matches.append(Vector2(poly_index, vertex_index))
                if current:  # if the current object then we can just exit the loop
                    return Vector2(poly_index, vertex_index)

    def view_logic(self):
        # inputs
        # shape controlls

        components_gui = pygame.sprite.Group()
        # panel
        panel_left_size = Vector2(250, self.app.win_height)
        panel_left = GuiPanel(Vector2(0, 0), panel_left_size, self.app, self.app.background, None, {})
        components_gui.add(panel_left)

        # button
        def action(event: dict, *_, **__):
            if 'MOUSE_LEFT' not in event:
                return
            # Make a new draw
            half_w = self.app.win_width / 2
            half_h = self.app.win_height / 2
            polygon = ShapeController.make_polygon(self.app, self.shape_new_vertex, 150, (half_w, half_h))
            self.polygons.append(polygon)

            # reset the new vertex counter
            self.shape_new_vertex = self.SHAPE_VERTEX_MIN

        btn_new_shape = GuiButton("New Shape", Vector2((panel_left_size.x / 2), 50), None,
                                  self.app, panel_left.image, panel_left, {})
        btn_new_shape.add_event_listener("click", action)
        # add child to panel
        panel_left.children_add(btn_new_shape)

        def vertex_add(event: dict, *_, **__):
            if 'MOUSE_LEFT' not in event:
                return

            self.shape_new_vertex += 1
            if self.shape_new_vertex > self.SHAPE_VERTEX_MAX:
                self.shape_new_vertex = self.SHAPE_VERTEX_MAX

        def vertex_remove(event: dict, *_, **__):
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

        def screen_clear(event: dict, *_, **__):
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

        def make_star(event: dict, *_, **__):
            if 'MOUSE_LEFT' not in event:
                return
            half_w = self.app.win_width / 4 + (len(self.stars) * len(self.stars))
            if len(self.stars) % 2 == 0:
                half_h = self.app.win_height / 2 - ((len(self.stars) * len(self.stars)) - 50)
            else:
                half_h = self.app.win_height / 2 + ((len(self.stars) * len(self.stars)) - 50)

            self.stars.append(ShapeController.make_polygon(self.app, 3, 150, (half_w, half_h)))

        def remove_star(event: dict, *_, **__):
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
        def view_about(event: dict, *_, **__):
            if 'MOUSE_LEFT' not in event:
                return
            self.app.view_current = "about"
            self.close_view = True

        button_navigate_about = GuiButton("About", Vector2((panel_left_size.x / 2), self.app.win_height - 70), None,
                                          self.app, panel_left.image, panel_left, {
                                              'background_color': pygame.Color("grey"),
                                              'border_color': pygame.Color("grey")
                                          })
        button_navigate_about.add_event_listener("click", view_about)
        # add child to panel
        panel_left.children_add(button_navigate_about)

        app_version = self.app.font_small.render(f'{self.app.app_info["__app__"]}', True, (255, 255, 255))


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

            panel_left.image.blit(app_version, Vector2(15, self.app.win_height - 30))

            if self.mode == 'polygon_selected' and self.current_selected_polygon is not None:
                polygon: Polygon = self.get_selected_polygon(self.current_selected_polygon)
                if not polygon:
                    self.keyboard_reset_selected_polygon()
                else:
                    self.gui_polygon_settings.render(polygon.centroid, polygon)


            # ---------------------------------------------------------
            # SHAPES
            # ---------------------------------------------------------
            if self.mode == 'polygon_selected' and self.current_selected_polygon is not None:
                hooked: bool = bool(
                    self._render_polygon(self.current_selected_polygon, mouse_current, None, is_selected=True))
            else:
                hooked: bool = self._render_polygons(mouse_current)

            # -------------------------------------------------------- #

            # ---------------------------------------------------------
            #   KEYBOARD / MOUSE CONTROL
            # ---------------------------------------------------------
            self.register_mouse_action(hooked)
            self.register_keyboard_action(hooked)

            # .............. drag center ............... #
            if self.current_figure_center is not None and self.current_figure_drag:
                ShapeController().move_polygon(self.polygons, self.current_figure_center, mouse_current)

            # .............. drag vertex ............... #
            elif self.current_figure and self.current_figure_drag:
                ShapeController.polygon_move_vertex(self.polygons, self.current_figure, (mouse_x, mouse_y))

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
    def get_selected_polygon(self, poly_index: int) -> Optional[Polygon]:
        """Retrieves the selected Polygon
        :param poly_index: int
        :return: Polygon|None
        """
        try:
            polygon: Polygon = self.polygons[poly_index]
        except IndexError as err:
            print(err)  # todo: print error in window!
            return None
        else:
            return polygon

    def vertex_dot_focus(self, polygon_index: Vector2) -> None:
        """Focus a Vertex, make it in a red dot

        :param polygon_index:
        :return:
        """
        try:
            polygon: Polygon = self.polygons[int(polygon_index.x)]
        except IndexError as err:
            print(str(err))
            return
        else:
            polygon.vertex_focus(int(polygon_index.y))

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
