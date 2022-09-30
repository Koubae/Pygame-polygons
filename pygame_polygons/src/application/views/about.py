import pygame
from pygame.math import Vector2

from ..gui import GuiPanel, GuiButton
from .view_manager import ViewManager

class ViewAbout(ViewManager):

    def __init__(self, *args):
        super().__init__(*args)

    def view_logic(self):

        components_gui = pygame.sprite.Group()
        # panel
        div_size = Vector2((self.app.win_width - 250, self.app.win_height - 150))
        div_pos = Vector2(self.app.win_width / 2 - (div_size.x / 2), self.app.win_height / 2 - (div_size.y / 2))
        div = GuiPanel(
            div_pos,
            div_size,
            self.app,
            self.app.background,
            None
        )
        components_gui.add(div)

        # button
        def view_home(event: dict, *_, **__):
            if 'MOUSE_LEFT' not in event:
                return
            self.app.view_current = "home"
            self.close_view = True


        btn_back_size: Vector2 = Vector2(120, 50)
        btn_back: GuiButton = GuiButton(
            "<-- Back to Home",
            Vector2(250 , 120),
            btn_back_size,
            self.app,
            div.image,
            div,
            {
                'background_color': (255, 25, 0, 85),
                'border_color': (255, 25, 0),
                'font_color': (255, 255, 255)
            }

        )
        btn_back.add_event_listener("click", view_home)
        components_gui.add(btn_back)
        print(__version__)

        about_text1 = """This Application is created by Federico Bau federicobau.dev © Copyright 2022"""
        font_img = self.app.font.render(about_text1, True, (255, 255, 255))
        about_text2 = """and is used for creating Pygame GUI applications or just add GUI functionalities to a Pygame Game"""
        font_img2 = self.app.font.render(about_text2, True, (255, 255, 255))

        def _update():
            components_gui.draw(self.app.background)
            components_gui.update()

            div.image.blit(font_img, (50, 150))
            div.image.blit(font_img2, (50, 175))

        return _update