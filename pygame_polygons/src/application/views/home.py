from math import pi, cos, sin

import pygame
from pygame.math import Vector2
from typing import Optional
from ..gui import GuiPanel, GuiButton
from .view_manager import ViewManager


def draw_regular_polygon(vertex_count, radius, position):
    """@credit: https://stackoverflow.com/a/57638991/13903942 """
    n, r = vertex_count, radius
    x, y = position
    return [
        Vector2(x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
        for i in range(n)
    ]


class ViewHome(ViewManager):

    def __init__(self, *args):
        super().__init__(*args)

    def view_logic(self):
        # inputs
        # shape controlls
        shape_vertex_min: int = 3
        shape_vertex_max: int = 100
        shape_new_vertex: int = 3

        components_gui = pygame.sprite.Group()
        # panel
        panel_left_size = Vector2(250, self.app.win_height)
        panel_left = GuiPanel(Vector2(0, 0), panel_left_size, self.app, self.app.background, None, {})
        components_gui.add(panel_left)

        polygons = []
        stars: list = []

        # button
        def action(event: dict):
            nonlocal shape_new_vertex
            if 'MOUSE_LEFT' not in event:
                return
            # Make a new draw
            half_w = self.app.win_width / 2
            half_h = self.app.win_height / 2
            polygon = draw_regular_polygon(shape_new_vertex, 150, (half_w, half_h))
            polygons.append(polygon)

            # reset the new vertex counter
            shape_new_vertex = shape_vertex_min

        btn_new_shape = GuiButton("New Shape", Vector2((panel_left_size.x / 2), 50), None,
                                  self.app, panel_left.image, panel_left, {})
        btn_new_shape.add_event_listener("click", action)
        # add child to panel
        panel_left.children_add(btn_new_shape)

        def vertex_add(event: dict):
            nonlocal shape_new_vertex
            if 'MOUSE_LEFT' not in event:
                return

            shape_new_vertex += 1
            if shape_new_vertex > shape_vertex_max:
                shape_new_vertex = shape_vertex_max

        def vertex_remove(event: dict):
            nonlocal shape_new_vertex
            if 'MOUSE_LEFT' not in event:
                return

            shape_new_vertex -= 1
            if shape_new_vertex < shape_vertex_min:
                shape_new_vertex = shape_vertex_min

        # add the shape vertex imput
        font = pygame.font.SysFont("Ariel", 24)
        font_small = pygame.font.SysFont("Roboto", 20)

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
            polygons.clear()
            stars.clear()

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
            nonlocal stars
            half_w = self.app.win_width / 4 + (len(stars) * len(stars))
            if len(stars) % 2 == 0:
                half_h = self.app.win_height / 2 - ((len(stars) * len(stars)) - 50)
            else:
                half_h = self.app.win_height / 2 + ((len(stars) * len(stars)) - 50)

            stars.append(draw_regular_polygon(3, 150, (half_w, half_h)))

        def remove_star(event: dict):
            if 'MOUSE_LEFT' not in event:
                return
            nonlocal stars
            stars.pop()

        btn_star = GuiButton("Make star", Vector2((panel_left_size.x / 2), 450), None,
                                     self.app, panel_left.image, panel_left, {})
        btn_star.add_event_listener("click", make_star)
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

        current_figure = ()
        current_figure_center = None
        current_figure_drag = False
        current_figure_wheel = False

        def _update():
            nonlocal current_figure
            nonlocal current_figure_center
            nonlocal current_figure_drag
            nonlocal current_figure_wheel
            nonlocal stars

            components_gui.draw(self.app.background)
            components_gui.update()

            about_text1 = f"Vertex = {shape_new_vertex}"
            font_img = font.render(about_text1, True, (255, 255, 255))
            panel_left.image.blit(font_img, Vector2((panel_left_size.x / 2 - (font_img.get_rect().width / 2)), 100))

            # make draws
            mouse_current = pygame.mouse.get_pos()
            mouse_x = mouse_current[0]
            mouse_y = mouse_current[1]

            hooked = False
            for poly_index, poly in enumerate(polygons):
                vertices_x = [v[0] for v in poly]
                vertices_y = [v[1] for v in poly]
                centroid = (sum(vertices_x) / len(poly), sum(vertices_y) / len(poly)) # finds the center of a polygon
                pygame.draw.circle(self.app.background, (79, 0, 153),  # draw red dot around vertex
                                   Vector2(centroid[0], centroid[1]), 5)
                pygame.draw.polygon(self.app.background, pygame.Color("green"), poly, width=2)




                matches = []
                matches_current = None
                # First, wee need to collect all vertex and check if there is a match. That's because
                # we need to know whether the user is still draggin the same vertex around. Else if we have a match
                # the new match found is the new vertex.
                for vertex_index, vertex in enumerate(poly):
                    vertex_x = vertex[0]
                    vertex_y = vertex[1]

                    # write vertex coordinates into the vertex
                    about_text1 = f"X={round(vertex_x, 2)}Y={round(vertex_y, 2)}"
                    font_img = font_small.render(about_text1, True, (153, 153, 255))
                    self.app.background.blit(font_img,
                                             Vector2(vertex_x + 5, vertex_y + 5))

                    margin = 3
                    current = False
                    if current_figure_drag and current_figure and current_figure[0] == poly_index and current_figure[1] == vertex_index:
                        # draggin multiplier
                        # fast user (like me) that move the mouse quick will notice that, so we need to
                        # increase the mouse area otherwise as soon as the mouse moves too fast, the vertex
                        # won't follow the mouse pointer and stops following it!
                        margin *= 55
                        current = True

                    # we check how distance is the vertex
                    vertex_x_diff = abs(mouse_x - vertex_x)
                    vertex_y_diff = abs(mouse_y - vertex_y)
                    if vertex_y_diff < margin and vertex_x_diff < margin:  # give some pixel of margin
                        matches.append((poly_index, vertex_index))
                        if current:
                            matches_current = (poly_index, vertex_index)
                            break

                if not hooked:
                    # first we check the center, if is grabbed then it has priority over vertices
                    margin = 3
                    if current_figure_center == poly_index:
                        # draggin multiplier
                        # fast user (like me) that move the mouse quick will notice that, so we need to
                        # increase the mouse area otherwise as soon as the mouse moves too fast, the vertex
                        # won't follow the mouse pointer and stops following it!
                        margin *= 25

                    vertex_x_diff = abs(mouse_x - centroid[0])
                    vertex_y_diff = abs(mouse_y - centroid[1])
                    if vertex_y_diff < margin and vertex_x_diff < margin:  # give some pixel of margin
                        hooked = True
                        current_figure = ()
                        current_figure_center = poly_index
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                        continue

                    if matches_current:
                        hooked = True
                        current_figure = matches_current
                        current_figure_center = None
                        vertex = polygons[matches_current[0]][matches_current[1]]
                        pygame.draw.circle(self.app.background, (255, 0, 0), # draw red dot around vertex
                                           Vector2(vertex[0], vertex[1]), 5)
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)

                        continue

                    if matches:
                        hooked = True
                        match = matches[0] # todo: should get the vertex with closest to mouse and not the first found
                        vertex = polygons[match[0]][match[1]]
                        pygame.draw.circle(self.app.background, (255, 0, 0), # draw red dot around vertex
                                           Vector2(vertex[0], vertex[1]), 5)
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
                        current_figure = (match[0], match[1])
                        current_figure_center = None

            if not hooked:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                current_figure = ()
                current_figure_center = None

            if pygame.MOUSEWHEEL in self.app.event_listener.events:  # mouse wheel
                pos = self.app.event_listener.events[pygame.MOUSEWHEEL]

                if 'WHEEL_UP' in pos:
                    current_figure_wheel = 'WHEEL_UP'
                elif 'WHEEL_DOWN' in pos:
                    current_figure_wheel = 'WHEEL_DOWN'
                else:
                    current_figure_wheel = None
            elif pygame.MOUSEWHEEL not in self.app.event_listener.events:
                current_figure_wheel = None

            if not current_figure_wheel and pygame.MOUSEBUTTONDOWN in self.app.event_listener.events:    # mouse press and drag
                current_figure_drag = True
            elif not current_figure_wheel and pygame.MOUSEBUTTONUP in self.app.event_listener.events:    # mouse release
                current_figure = ()

                current_figure_center = None
                current_figure_drag = False


            if current_figure_center is not None and current_figure_drag:
                # Drags the polygon aounr: todo: improve this
                polygon = polygons[current_figure_center]
                vertices_x = [v[0] for v in polygon]
                vertices_y = [v[1] for v in polygon]
                centroid = (
                    sum(vertices_x) / len(polygon), sum(vertices_y) / len(polygon))  # finds the center of a polygon
                for vertex_index, vertex in enumerate(polygon):
                    vertex_x_diff = mouse_x - centroid[0]
                    vertex_y_diff = mouse_y - centroid[1]
                    polygon[vertex_index][0] += vertex_x_diff
                    polygon[vertex_index][1] += vertex_y_diff


            elif current_figure and current_figure_drag:
                polygons[current_figure[0]][current_figure[1]] = Vector2(mouse_x, mouse_y)

            if current_figure_center is not None and current_figure_wheel:
                # Drags the polygon aounr: todo: improve this
                polygon = polygons[current_figure_center]
                vertices_x = [v[0] for v in polygon]
                vertices_y = [v[1] for v in polygon]
                centroid = (
                    sum(vertices_x) / len(polygon), sum(vertices_y) / len(polygon))  # finds the center of a polygon
                polygon_rotated = []

                angle = .2
                if current_figure_wheel == 'WHEEL_DOWN':
                    angle = -angle

                for vertex_index, vertex in enumerate(polygon):
                    v_x = centroid[0] + ((vertex[0] - centroid[0]) * cos(angle)) - ((vertex[1] - centroid[1]) * sin(angle))
                    v_y = centroid[1] + ((vertex[0] - centroid[0]) * sin(angle)) + ((vertex[1] - centroid[1]) * cos(angle))
                    polygon_rotated.append(Vector2(v_x, v_y))
                polygons[current_figure_center] = polygon_rotated

            # Make star
            if stars:
                # make the star roating continously making double adges
                for i, star in enumerate(stars):
                    vertices_x = [v[0] for v in star]
                    vertices_y = [v[1] for v in star]
                    centroid = (sum(vertices_x) / len(star), sum(vertices_y) / len(star))  # finds the center of a polygon
                    pygame.draw.circle(self.app.background, (79, 0, 153),  # draw red dot around vertex
                                       Vector2(centroid[0], centroid[1]), 5)
                    pygame.draw.polygon(self.app.background, pygame.Color("pink"), star, width=2)
                    star_rotated = []
                    for vertex_index, vertex in enumerate(star):
                        v_x = centroid[0] + ((vertex[0] - centroid[0]) * cos(45)) - ((vertex[1] - centroid[1]) * sin(45))
                        v_y = centroid[1] + ((vertex[0] - centroid[0]) * sin(45)) + ((vertex[1] - centroid[1]) * cos(45))
                        star_rotated.append(Vector2(v_x, v_y))
                    stars[i] = star_rotated


        return _update
