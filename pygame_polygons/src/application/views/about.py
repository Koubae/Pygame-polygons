import pygame
from pygame.math import Vector2

from ..gui import GuiPanel
from .view_manager import ViewManager

class ViewAbout(ViewManager):

    def __init__(self, *args):
        super().__init__(*args)

    def view_logic(self):

        components_gui = pygame.sprite.Group()
        # panel
        div_size = Vector2((self.app.win_width - 250, self.app.win_height - 150))
        div_pos = Vector2(self.app.win_width / 2 - (div_size.x / 2), self.app.win_height / 2 - (div_size.y / 2))
        div = GuiPanel(div_pos, div_size, self.app, self.app.background, None)
        div.mouse_pointer = pygame.SYSTEM_CURSOR_HAND
        components_gui.add(div)

        # button
        def view_home(event: dict):
            if 'MOUSE_LEFT' not in event:
                return
            self.app.view_current = "home"
            self.close_view = True

        div.add_event_listener("click", view_home)
        print("hello")


        about_text1 = """This Application is created by Federico Bau federicobau.dev © Copyright 2022"""
        font = pygame.font.SysFont("Ariel", 24)
        font_img = font.render(about_text1, True, (255, 255, 255))
        about_text2 = """and is used for creating Pygame GUI applications or just add GUI functionalities to a Pygame Game"""
        font_img2 = font.render(about_text2, True, (255, 255, 255))

        def _update():
            components_gui.draw(self.app.background)
            components_gui.update()

            div.image.blit(font_img, (50, 50))
            div.image.blit(font_img2, (50, 75))

        return _update