from typing import Optional
import pygame
from .application.services.event_listener import EventListener

class App:
    DEFAULT_DISPLAY: int = 0

    def __init__(self, app_name: str, app: dict, world: dict, ):
        self.app_name: str = app_name
        self.run: bool = True
        # App data
        self.clock: pygame.time.Clock = app["clock"]
        self.frames: int = app["frames"]

        # world data
        self.display_info: pygame.display.Info = world["display_info"]
        self.screen_size: str = world["screen_size"]
        self.screen_size_type: str = world["screen_size_type"]
        self.display_width: int = world["display_width"]
        self.display_height: int = world["display_height"]

        self.win_flags: int = 0
        self.win_size: tuple = world["win_size"]
        self.win_width: int = world["win_width"]
        self.win_height: int = world["win_height"]
        self.chunk: int = world["chunk"]

        window, background = self.create_app()

        self.window: pygame.Surface = window
        self.background: pygame.Surface = background

        self.event_listener: EventListener = EventListener(self)

        # views
        self.view_current: Optional[str] = None

    def create_app(self) -> tuple:
        pygame.display.set_caption(self.app_name)
        # screen
        if self.screen_size == "large":
            self.win_flags = pygame.NOFRAME

        window = pygame.display.set_mode(self.win_size, self.win_flags, 32, display=self.DEFAULT_DISPLAY)
        background = pygame.Surface(self.win_size)
        return window, background

    def switch_off(self):
        """Stops the execution of the application. Add here any clean-up """
        self.run = False
        # ... clean-up resource , close db connections etc...

