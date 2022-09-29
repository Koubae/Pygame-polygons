import pygame
from pygame.math import Vector2
from typing import Optional

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
        self.window.children_add(self.color_picker_btn_background)
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
        self.window.children_add(self.color_picker_btn_border)
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
        self.window.children_add(self.color_picker)

        self.cp: ColorPicker = ColorPicker(0, 0, 150, 12)

        self.color_picker_colors: list[tuple[GuiButton, tuple]] = []
        colors = {
            'custom': self.cp.get_color(),
            **Polygon.TERMINAL_COLORS,
            'no_color': self.DEFAULT_WINDOW_BACKGROUND_COLOR
        }
        for color, rgb in colors.items():
            # Create a button
            btn_size: Vector2 = Vector2(75, 15)
            btn: GuiButton = GuiButton(
                color,
                Vector2((self.window_size.x - 50), 10),
                btn_size,
                self.app,
                self.window.image,
                self.window, {
                    'background_color': (rgb[0], rgb[1], rgb[2], 55),
                    'border_color': rgb,
                    'font_color': rgb
                }
            )

            self.gui_group.add(btn)
            self.window.children_add(btn)
            btn.add_event_listener("click", self.change_polygon_color, rgb)

            self.color_picker_colors.append((btn, rgb))

        self.margin_width_slider: Slider = Slider(0, 0, 150, 8)

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
        if polygon is not self.polygon_current:
            self._clean_up(polygon)
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

    def _clean_up(self, polygon:Polygon):
        super()._clean_up()

        self.margin_width_slider =  Slider(0, 0, 150, 8)
        self.margin_width_slider.slide_value = polygon.border_width

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
        self.color_picker_mode = color_mode

    def change_polygon_color(self, _: dict, color: tuple, *__, **___) -> None:
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