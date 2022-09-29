import pygame
from pygame.math import Vector2
from typing import Optional

from ...shapes import Polygon
from ....application.gui import GuiPanel, GuiButton, GuiComponent


class PolygonSettingWindow(GuiComponent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------
        # Polygon context window
        self.color_picker_size: Vector2 = Vector2(50, 50)
        self.color_picker: GuiPanel = GuiPanel(
            Vector2(50, 50),
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

        self.color_picker_colors: list[tuple[pygame.font.Font, tuple]] = []
        for color, rgb in Polygon.TERMINAL_COLORS.items():
            text = self.app.font_gui.render(
                color.replace("_", " ").capitalize(),
                True,
                rgb
            )
            self.color_picker_colors.append((text, rgb))


    def _pre_render(self, polygon: Polygon, *args, **kwargs) -> None:
        """@ovverride

        :param polygon: Polygon
        :param args:
        :param kwargs:
        :return:
        """
        super()._pre_render( *args, **kwargs)

        self.color_picker.move_gui_into(Vector2(self.window_position.x + 50, self.window_position.y + 50))

        for i, (color, rgb) in enumerate(self.color_picker_colors):
            self.window.image.blit(
                color,
                Vector2(self.window_position.x + 100, i * (self.window_position.y + 50))
            )