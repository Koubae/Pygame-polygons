import sys
import pygame
from ...app import App


class ViewManager:

    def __init__(self, app: App):
        self.app: App = app
        self.close_view: bool = False

    def screen_clear(self):
        self.app.background.fill(pygame.Color("black"))

    def screen_paint(self):
        self.app.window.blit(self.app.background, (0, 0))

    def game_update(self):
        pygame.display.update()

    def game_tick(self):
        self.app.clock.tick(self.app.frames)

    def events_handler(self):
        self.app.event_listener.events_listen()

    def clean_up_resources(self, *args, **kwargs):
        """@overide"""
        pass

    def view_logic(self):

        def _update():
            pass

        return _update

    def game_beat(self):
        self._reinit_view()
        game_update = self.view_logic()
        while self.app.run:
            if self.close_view:
                self._reset_view()
                return  # exit without break the loop!
            self.screen_clear()  # screen clear

            # ==============================================================================
            #                               GAME LOGIC HERE
            # ==============================================================================

            # ....
            game_update()

            # ==============================================================================
            # ..............................................................................
            # ==============================================================================

            # This in order
            self.events_handler()  # 1) Events
            self.game_update()  # 2) Update the game
            self.screen_paint()  # 3) Repaint the screen
            self.game_tick()  # 4) Wait 60 Frames

        # Do some resource clean up ...
        self.clean_up_resources()


    def _reinit_view(self):
        """Perform intial view set-up"""
        self.close_view = False  #


    def _reset_view(self):
        """Perform clean up of the view"""
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
