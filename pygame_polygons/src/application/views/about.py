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
            Vector2(250, 120),
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
        app_info = self.app.app_info
        about_text = f"""
        A Pygame Application done to build more Pygame applications / games
        Basically I needed a tool that would easily make me able to draw shapes / Polygons on a Pygame screen and be able to
        quickly see the vertices x,y coordinates.
        
        Because you can also move the polygons around, this provide a good way to test and get move draw quick into a new
        Pygame project where drawing polygons is needed, because it shows you the coordinates on the screen.
        
        Author:
        
        This Application is created by {app_info['__author__']}, a Software developer, feel free to visit {app_info['__website__']}
        {app_info['__author__']} {app_info['__copyright__']}    
        {app_info['__app__']}    
        """

        font_imgs = []
        for line in about_text.split('\n'):
            font_imgs.append(self.app.font.render(line, True, (255, 255, 255)))

        def _update():
            components_gui.draw(self.app.background)
            components_gui.update()

            for i, text in enumerate(font_imgs):
                div.image.blit(text, (50, 150 + ( i * 25)))



        return _update
