import pygame 
from pygame.math import Vector2

from ...config.constants import *

from .gui_panel import GuiPanel


class GuiButton(GuiPanel):
    DEFAULT_BUTTON_SIZE: Vector2 = Vector2(150, 35)

    def __init__(self, text: str, *args):
        if not args[1]:
            args = list(args)
            args[1] = self.DEFAULT_BUTTON_SIZE
        # center the entity by x
        args[0].x -= args[1].x / 2

        super().__init__(*args)

        # if style_inherit_parent is True then gets the default Settings from Parent
        if "style_inherit_parent" not in self.settings or self.settings["style_inherit_parent"] != True:
            setting_panel = GUI_STYLES["gui"]["button"]

            self.background_color: tuple = "background_color" in self.settings and self.settings["background_color"] or \
                                           setting_panel["background_color"]
            self.border_color: tuple = "border_color" in self.settings and self.settings["border_color"] or \
                                       setting_panel[
                                           "border_color"]
            self.border_radius: int = "border_radius" in self.settings and self.settings["border_radius"] or \
                                      setting_panel[
                                          "border_radius"]
            self.border_width: int = "border_width" in self.settings and self.settings["border_width"] or setting_panel[
                "border_width"]

            self.register_default_element_values()  # re-register default values

        self.text: str = text
        self.text_img = self.font.render(self.text, True, self.font_color)

        # events
        self.mouse_pointer = pygame.SYSTEM_CURSOR_HAND

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        # check if is clicked
        if self.mouse_action == "MOUSE_ENTERED":
            events = self.app.event_listener.events
            if pygame.MOUSEBUTTONDOWN in events:
                button_clicks = events[pygame.MOUSEBUTTONDOWN]
                if "MOUSE_LEFT" in button_clicks and not self.element_clicked:
                    self.surface_clear()  # makes the button 'light-turn off'
                    topleft = self.rect.topleft
                    # makes button go down givin the impression that is pressed
                    self.rect = self.image.get_rect().move(topleft[0], topleft[1] + 3)
                    self.element_clicked = True
                    self.element_clicked_timer = 8
        if self.element_clicked:
            if self.element_clicked_timer <= 0:
                self.element_clicked = False
                self.element_clicked_timer = 0
                topleft = self.rect.topleft
                self.rect = self.image.get_rect().move(topleft[0], topleft[1] - 3)
            else:
                self.element_clicked_timer -= 1

        # render text
        self.image.blit(self.text_img, self.text_img.get_rect(center=self.image.get_rect().center))

    def _on_mouse_enter(self):
        super()._on_mouse_enter()
        if self.mouse_action != "MOUSE_ENTERED":
            return

        # if not the same, new lighten background was set
        if self.background_color != self.background_color_default:
            return

        # ligth-up the background color
        new_background = []
        for c in self.background_color:
            new_color = c + 75
            if new_color > 250:
                new_color = 250
            new_background.append(new_color)
        self.background_color = tuple(new_background)

        new_border_color = []
        for c in self.border_color:
            new_c = c + 75
            if new_c > 250:
                new_c = 250
            new_border_color.append(new_c)
        self.border_color = tuple(new_border_color)

    def _on_mouse_leave(self):
        super()._on_mouse_leave()
        if self.mouse_action != "MOUSE_LEAVED":
            return
        self.background_color = self.background_color_default
        self.border_color = self.border_color_default


