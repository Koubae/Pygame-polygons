from pygame.math import Vector2
from typing import Optional
import traceback
from ...shapes import Polygon
from ....application.gui import GuiButton, GuiComponent
from .color_picker import ColorPicker
from .slider import Slider


class PolygonSettingWindow(GuiComponent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.polygon_current: Optional[Polygon] = None

        # -------------------
        # Polygon context window

        # ----------------------------
        # Color Settings

        self.color_picker_modes: tuple[str, str] = ('background', 'border')
        self.color_picker_mode: str = self.color_picker_modes[1]

        self.color_picker_btn_mode_size: Vector2 = Vector2(110, 25)
        self.color_picker_btn_background: GuiButton = GuiButton(
            "Background",
            Vector2((self.window_size.x - 150), 10),
            self.color_picker_btn_mode_size,
            self.app,
            self.window.image,
            self.window,
            {
                'background_color': self.DEFAULT_WINDOW_BACKGROUND_COLOR,
                'font_color': (125, 125, 125)
            }
        )
        self.gui_group.add(self.color_picker_btn_background)
        self.color_picker_btn_background.add_event_listener("click", self.color_picker_set_mode,
                                                            self.color_picker_modes[0])

        self.color_picker_btn_border: GuiButton = GuiButton(
            "Border",
            Vector2((self.window_size.x - 100), 10),
            self.color_picker_btn_mode_size,
            self.app,
            self.window.image,
            self.window,
            {
                'background_color': self.DEFAULT_WINDOW_BACKGROUND_COLOR,
                'font_color': (125, 125, 125)
            }
        )
        self.gui_group.add(self.color_picker_btn_border)
        self.color_picker_btn_border.add_event_listener("click", self.color_picker_set_mode, self.color_picker_modes[1])

        self.color_picker_size: Vector2 = Vector2(50, 50)
        self.color_picker: GuiButton = GuiButton(
            "",
            Vector2(25, 50),
            self.color_picker_size,
            self.app,
            self.app.background,
            self.window,
            {
                'background_color': (255, 255, 0),
                'border_color': (255, 255, 0)
            }

        )
        self.gui_group.add(self.color_picker)

        self.cp: ColorPicker = ColorPicker(0, 0, 150, 12)

        self.color_picker_colors: list[tuple[GuiButton, tuple]] = []
        colors = {
            'custom': self.cp.get_color(),
            **Polygon.TERMINAL_COLORS,
            'no_color': self.DEFAULT_WINDOW_BACKGROUND_COLOR
        }
        for color, rgb in colors.items():
            # Create a button
            btn_size: Vector2 = Vector2(75, 20)
            btn: GuiButton = GuiButton(
                color.replace('_', ' ').capitalize(),
                Vector2((self.window_size.x - 50), 10),
                btn_size,
                self.app,
                self.window.image,
                self.window,
                {
                    'background_color': (rgb[0], rgb[1], rgb[2], 55),
                    'border_color': rgb,
                    'font_color': rgb
                }
            )

            self.gui_group.add(btn)
            btn.add_event_listener("click", self.change_polygon_color, rgb)

            self.color_picker_colors.append((btn, rgb))

        self.margin_width_slider: Slider = Slider(0, 0, 150, 8)

        # ----------------------------
        # Shape Settings

        self.btn_vertex: Vector2 = Vector2(25, 25)
        self.btn_vertex_add: GuiButton = GuiButton(
            "+",
            Vector2(25, 50),
            self.btn_vertex,
            self.app,
            self.app.background,
            self.window,

        )
        self.gui_group.add(self.btn_vertex_add)
        self.btn_vertex_add.add_event_listener("click", self.vertex_add)

        self.btn_vertex_remove: GuiButton = GuiButton(
            "-",
            Vector2(25, 50),
            self.btn_vertex,
            self.app,
            self.app.background,
            self.window,

        )
        self.gui_group.add(self.btn_vertex_remove)
        self.btn_vertex_remove.add_event_listener("click", self.vertex_remove)

        self.btn_remove_all_size: Vector2 = Vector2(75, 25)
        self.btn_remove_all: GuiButton = GuiButton(
            "-- Vertex",
            Vector2(25, 50),
            self.btn_remove_all_size,
            self.app,
            self.app.background,
            self.window,

        )
        self.gui_group.add(self.btn_remove_all)
        self.btn_remove_all.add_event_listener("click", self.vertex_remove_all)

        self.btn_reset_size: Vector2 = Vector2(75, 25)
        self.btn_reset: GuiButton = GuiButton(
            "Reset",
            Vector2(25, 50),
            self.btn_reset_size,
            self.app,
            self.app.background,
            self.window,
            {
                'background_color': (255, 25, 0, 85),
                'border_color': (255, 25, 0),
                'font_color': (255, 255, 255)
            }

        )
        self.gui_group.add(self.btn_reset)
        self.btn_reset.add_event_listener("click", self.vertex_reset)

    def _render(self):
        super()._render()

        self._render_color_picker()
        self._render_margin_width_slider()

    def _pre_render(self, polygon: Polygon, *args, **kwargs) -> None:
        """@ovverride

        :param polygon: Polygon
        :param args:
        :param kwargs:
        :return:
        """
        super()._pre_render(*args, **kwargs)
        if self.polygon_current and polygon is not self.polygon_current:
            self._clean_up()
        self.polygon_current = polygon

        # ----------------------------
        # Color Settings

        polygon.border_width = self.margin_width_slider.slide_value

        custom_color = self.cp.current_color
        custom_color_btn = self.color_picker_colors[0][0]

        custom_color_btn.remove_event_listeners("click")
        custom_color_btn.add_event_listener("click", self.change_polygon_color, custom_color)
        custom_color_btn.background_color_default = [custom_color[0], custom_color[1], custom_color[2], 55]
        custom_color_btn.border_color_default = custom_color

        if polygon.background_color:
            self.color_picker.background_color_default = polygon.background_color
        self.color_picker.border_color_default = polygon.border_color
        self.color_picker.move_gui_into(Vector2(self.window_position.x + 50, self.window_position.y + 50))

        if self.color_picker_mode == 'background':
            self.color_picker_btn_background.background_color_default = (255, 255, 255)
            self.color_picker_btn_background.change_text_color((0, 0, 0))

            self.color_picker_btn_border.background_color_default = self.DEFAULT_WINDOW_BACKGROUND_COLOR
            self.color_picker_btn_border.change_text_color((125, 125, 125))

        else:
            self.color_picker_btn_border.background_color_default = (255, 255, 255)
            self.color_picker_btn_border.change_text_color((0, 0, 0))

            self.color_picker_btn_background.background_color_default = self.DEFAULT_WINDOW_BACKGROUND_COLOR
            self.color_picker_btn_background.change_text_color((125, 125, 125))

        # render color picker mode btns
        self.color_picker_btn_background.move_gui_into(
            Vector2(self.window_position.x + 50, self.window_position.y + 15))
        self.color_picker_btn_border.move_gui_into(
            Vector2(self.window_position.x + 50 + self.color_picker_btn_mode_size.x, self.window_position.y + 15))

        for i, (color, rgb) in enumerate(self.color_picker_colors):
            color.move_gui_into(
                Vector2(
                    self.window_position.x + 125,
                    (i * 20) + self.window_position.y + 45
                )
            )

        # ----------------------------
        # Shape Settings

        self.btn_vertex_add.move_gui_into(Vector2(self.window_position.x + 50, self.window_position.y + 120))
        self.btn_vertex_remove.move_gui_into(Vector2(self.window_position.x + 80, self.window_position.y + 120))

        self.btn_remove_all.move_gui_into(Vector2(self.window_position.x + 50, self.window_position.y + 155))
        self.btn_reset.move_gui_into(Vector2(self.window_position.x + 50, self.window_position.y + 185))

    def _clean_up(self, *args, **kwargs):
        super()._clean_up()
        self.polygon_current = None
        self.view.current_selected_polygon = None

        # TODO fixme currently the initial value of the slider cannot be set, it will alsway start from value 0
        # self.margin_width_slider.set_slider_value(polygon.border_width)

        # reset custom color picker
        custom_color = self.cp.get_color(first_value=True)
        custom_color_btn = self.color_picker_colors[0][0]
        custom_color_btn.remove_event_listeners("click")
        custom_color_btn.add_event_listener("click", self.change_polygon_color, custom_color)
        custom_color_btn.background_color_default = [custom_color[0], custom_color[1], custom_color[2], 55]
        custom_color_btn.border_color_default = custom_color

        # reset default color pickers
        self.color_picker_mode: str = self.color_picker_modes[1]
        self.color_picker.background_color_default = (255, 255, 0)
        self.color_picker.border_color_default = (255, 255, 0)

        self.color_picker_btn_border.background_color_default = (255, 255, 255)
        self.color_picker_btn_border.change_text_color((0, 0, 0))

        self.color_picker_btn_background.background_color_default = self.DEFAULT_WINDOW_BACKGROUND_COLOR
        self.color_picker_btn_background.change_text_color((125, 125, 125))

    # ---------------------
    # Settings methods
    # ---------------------

    # ----------------------------
    # Color Settings

    def _render_color_picker(self) -> None:
        """Render to Component window the Color picker"""
        cp_pos: Vector2 = Vector2(
            Vector2(self.window_position.x + 125 + 90, self.window_position.y + 45)
        )
        self.cp.rect.topleft = cp_pos
        self.cp.image.get_rect(topleft=cp_pos)
        self.cp.update()
        self.cp.draw(self.screen)

    def color_picker_set_mode(self, _: dict, color_mode: str, *__, **___) -> None:
        """Set the picker color mode"""
        self.color_picker_mode = color_mode

    def change_polygon_color(self, _: dict, color: tuple, *__, **___) -> None:
        """Change the polygon background color or border color, depending on the current mode"""
        if not self.polygon_current:
            return

        if self.color_picker_mode == 'background':
            if color == self.DEFAULT_WINDOW_BACKGROUND_COLOR:
                color = None  # reset the color
            self.polygon_current.background_color = color
        else:
            if color == self.DEFAULT_WINDOW_BACKGROUND_COLOR:
                color = self.color_picker_colors[0][1]  # reset the color

            self.polygon_current.border_color = color

    def _render_margin_width_slider(self) -> None:
        """Render to Component window the Color picker"""
        pos: Vector2 = Vector2(
            Vector2(self.window_position.x + 125 + 90, self.window_position.y + 65)
        )
        self.margin_width_slider.rect.topleft = pos
        self.margin_width_slider.image.get_rect(topleft=pos)
        self.margin_width_slider.update()
        self.margin_width_slider.draw(self.screen)

    # ----------------------------
    # Shape Settings

    def vertex_add(self, event: dict, *_, **__):
        """Adds one vertex
            TODO: User should be able ALSO to add a vertex at desired position (meaning at index i, y ...)
        """
        if 'MOUSE_LEFT' not in event:
            return

        # TODO: FIXME there must ba a mathematical formula to add and calcualte a new vertex in a polygon.
        # Currenty it works BUT when the len of vertices is inferior to the index of the next vertix, is skippin a possition
        # of the new vertx in a wrong place. see tag # FIXME_IS_BROKEN:( where the code does not work!

        polygon: Polygon = self.polygon_current

        # Increase the vertices count and get new vertices
        polygon.vertex_count += 1
        vertices: list[Vector2] = Polygon.draw_regular_polygon(polygon.vertex_count, polygon.radius, polygon.centroid)

        # now we need to determine the new vertex position
        vertices_added_current = polygon.vertices_added
        vertices_added_total = len(vertices_added_current)
        if not vertices_added_total:
            add_vertex_in = 1
            polygon.vertices_added = [(1, vertices[0])]
        else:
            get_latest_added_vertex = vertices_added_current[-1]
            latest_index = get_latest_added_vertex[0]

            add_vertex_in = (latest_index + 2)
            if add_vertex_in == len(vertices) - 2:
                add_vertex_in = len(vertices) - 1
            elif add_vertex_in >= len(vertices) - 1:  # FIXME_IS_BROKEN:(
                add_vertex_in = 1

            try:
                polygon.vertices_added.append((add_vertex_in, vertices[add_vertex_in]))
            except IndexError as err:
                print(err)
                traceback.print_exc()

        vertices_current = polygon.vertices
        try:
            vertices_current.insert(add_vertex_in, vertices[add_vertex_in])
        except IndexError as err:
            print(err)
            traceback.print_exc()

        polygon.vertices = vertices_current

    def vertex_remove(self, event: dict, *_, **__):
        """Removes latest added vertix"""
        if 'MOUSE_LEFT' not in event:
            return
        polygon: Polygon = self.polygon_current
        if polygon.vertex_count == 3 or not polygon.vertices_added:
            return
        polygon.vertex_count -= 1
        polygon_vertices = polygon.vertices

        vertices_added_current = polygon.vertices_added
        get_latest_added_vertex = vertices_added_current.pop()
        latest_index = get_latest_added_vertex[0]
        polygon_vertices.pop(latest_index)  # remove last inserted vertex
        polygon.vertices = polygon_vertices

    def vertex_remove_all(self, event: dict, *_, **__):
        """Remove all added vertices to the polygon however the original vertices x,y position won't change"""
        if 'MOUSE_LEFT' not in event:
            return

        polygon: Polygon = self.polygon_current
        if polygon.vertex_count == 3 or not polygon.vertices_added:
            return
        polygon.vertex_count -= len(polygon.vertices_added)
        polygon_vertices = polygon.vertices

        for vertex_added in reversed(polygon.vertices_added):
            index = vertex_added[0]
            polygon_vertices.pop(index)  # remove last inserted vertex

        polygon.vertices_added.clear()
        polygon.vertices = polygon_vertices

    def vertex_reset(self, event: dict, *_, **__):
        """Reset the current Polygon to its initial values"""
        if 'MOUSE_LEFT' not in event:
            return
        polygon: Polygon = self.polygon_current
        polygon.vertices_reset()

