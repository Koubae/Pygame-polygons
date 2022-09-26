from __future__ import annotations
from pygame.math import Vector2

from ...config.constants import *
from ...app import App
from .gui_element import GuiElement


class GuiPanel(GuiElement):

    def __init__(self,
                 pos: Vector2,
                 size: Vector2,
                 app: App,
                 screen: pygame.Surface,
                 parent: GuiPanel = None,
                 settings: dict = None,
                 *args
                 ):

        settings: dict = settings and settings or {}
        if 'blit_type' not in settings:
            settings['blit_type'] = "draw"

        super().__init__(pos, size, app, screen, parent, settings, *args)

        # if style_inherit_parent is True then gets the default Settings from Parent
        if "style_inherit_parent" not in self.settings or self.settings["style_inherit_parent"] != True:
            setting_panel = GUI_STYLES["gui"]["panel"]

            self.settings: dict = settings and settings or {}
            self.background_color: tuple = "background_color" in self.settings and self.settings["background_color"] or \
                                           setting_panel["background_color"]
            self.border_color: tuple = "border_color" in self.settings and self.settings["border_color"] or \
                                       setting_panel[
                                           "border_color"]
            self.border_width: int = "border_width" in self.settings and self.settings["border_width"] or setting_panel[
                "border_width"]
            self.border_radius: int = "border_radius" in self.settings and self.settings["border_radius"] or \
                                      setting_panel[
                                          "border_radius"]

            self.register_default_element_values()  # re-register default values
