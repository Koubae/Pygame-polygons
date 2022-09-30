import os
from pygame.math import Vector2
from typing import Optional
from .application.services.event_listener import EventListener
from .config.constants import *
from .version import (
    __version__,
    __author__,
    __website__,
    __copyright__,
    __credits__,
    __license__,
    __maintainer__,
    __email__,
    __emails__,
    __status__,
    __app__
)


class App:
    DEFAULT_DISPLAY: int = 0

    def __init__(self, app_name: str, app: dict, world: dict, ):
        # laod app info
        self.app_info: dict = {
            "__version__": __version__,
            "__author__": __author__,
            "__website__": __website__,
            "__copyright__": __copyright__,
            "__credits__": __credits__,
            "__license__": __license__,
            "__maintainer__": __maintainer__,
            "__email__": __email__,
            "__emails__": __emails__,
            "__status__": __status__,
            "__app__": __app__,
        }

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

        # Load fonts
        self.font: pygame.font.SysFont = pygame.font.SysFont("Ariel", 24)
        self.font_small: pygame.font.SysFont = pygame.font.SysFont("lucidasans", 12)
        # gui fonts
        self.font_gui_family: str = GUI_STYLES["gui"]["font"]["font_family"]
        self.font_gui_size: int = GUI_STYLES["gui"]["font"]["font_size"]
        self.font_gui_color: tuple = GUI_STYLES["gui"]["font"]["font_color"]
        self.font_gui = pygame.font.SysFont(self.font_gui_family, self.font_gui_size)  # todo: move to app level !!!

        # views
        self.view_current: Optional[str] = None

    def create_app(self) -> tuple:
        pygame.display.set_caption(self.app_name)
        pygame.event.set_allowed([
            pygame.QUIT,
            pygame.KEYDOWN,
            pygame.KEYUP,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEWHEEL
        ])
        # screen
        if self.screen_size == "large":
            self.win_flags = pygame.NOFRAME | pygame.FULLSCREEN | pygame.DOUBLEBUF

        window = pygame.display.set_mode(self.win_size, self.win_flags, 32, display=self.DEFAULT_DISPLAY)
        background = pygame.Surface(self.win_size, pygame.SRCALPHA)

        # load the icon
        # app_icon = pygame.image.load(os.path.join(os.getcwd(), 'resources', 'icon.ico', )).convert()
        # app_icon = pygame.transform.scale(app_icon, (32, 32))
        # app_icon.set_colorkey((0, 0, 0))
        # pygame.display.set_icon(app_icon)

        return window, background

    def switch_off(self):
        """Stops the execution of the application. Add here any clean-up """
        self.run = False
        # ... clean-up resource , close db connections etc...

    def window_get_4_sides(self) -> dict:
        """determine the position of the center of the polygon, Is it in the
        we devide the screen in 4 (TOP-LEFT, TOP-RIGHT, BOTTOM-LEFT, BOTTOM-RIGHT) add set to opposite direction
        :return:
        """
        win_width, win_height = self.win_width, self.win_height
        return {
            'top_left': (Vector2(0, 0), Vector2(win_width / 2, win_height / 2)),
            'top_right': (Vector2(win_width / 2 + 1, 0), Vector2(win_width, win_height / 2)),
            'bottom_left': (Vector2(0, win_height / 2 + 1), Vector2(win_width / 2, win_height)),
            'bottom_right': (Vector2(win_width / 2 + 1, win_height / 2 + 1), Vector2(win_width, win_height))
        }

    def get_window_position_relative_to_coords(self, coords: Vector2) -> Optional[str]:
        """

        :param coords: Vector2
        :return: dict
        """
        # now, where are the x,y coordinates at?
        window_sides = self.window_get_4_sides()
        top_left: tuple[Vector2, Vector2] = window_sides["top_left"]
        top_right: tuple[Vector2, Vector2] = window_sides["top_right"]
        bottom_left: tuple[Vector2, Vector2] = window_sides["bottom_left"]
        bottom_right: tuple[Vector2, Vector2] = window_sides["bottom_right"]

        # now, where are the x,y coordinates at?
        position = {'top_left': False, 'top_right': False, 'bottom_left': False, 'bottom_right': False}
        if (coords.x >= top_left[0].x and coords.y >= top_left[0].y) and \
                (coords.x <= top_left[1].x and coords.y <= top_left[1].y):
            position['top_left'] = True
        elif (coords.x >= top_right[0].x and coords.y >= top_right[0].y) and \
                (coords.x <= top_right[1].x and coords.y <= top_right[1].y):
            position['top_right'] = True

        elif (coords.x >= bottom_left[0].x and coords.y >= bottom_left[0].y) and \
                (coords.x <= bottom_left[1].x and coords.y <= bottom_left[1].y):
            position['bottom_left'] = True
        elif (coords.x >= bottom_right[0].x and coords.y >= bottom_right[0].y) and \
                (coords.x <= bottom_right[1].x and coords.y <= bottom_right[1].y):
            position['bottom_right'] = True
        return next((k for k, v in position.items() if v), None)

    def get_window_opposite_position(self, coords: Vector2, entity_size: Vector2) -> Optional[Vector2]:
        """Given x,y cordinates and a possible entity x,y size determine at which
        position if currently in the window screen (top-left, top-right, bottom_left, botom_right)
        and then get the cooridnates of its new center position at the opposite side

        :param coords: Vector2 x,y coordinates
        :param entity_size: Vector2 x,y size (width,height)
        :return: None|Vector2 x,y coordinate of the new opposite position
        """
        window_sides = self.window_get_4_sides()
        top_left: tuple[Vector2, Vector2] = window_sides["top_left"]
        top_right: tuple[Vector2, Vector2] = window_sides["top_right"]
        bottom_left: tuple[Vector2, Vector2] = window_sides["bottom_left"]
        bottom_right: tuple[Vector2, Vector2] = window_sides["bottom_right"]

        position: Optional[str] = self.get_window_position_relative_to_coords(coords)
        if not position:
            return
        coord_opposite: Vector2
        if position == 'top_left':
            # go to top_right
            coord_opposite = Vector2(top_right[1].x / 2 + (entity_size.x / 4),
                                     top_right[1].y / 2)

        elif position == 'top_right':
            # go to top_left
            coord_opposite = Vector2(top_left[1].x / 2 - (entity_size.x / 2),
                                     top_left[1].y / 2)
        elif position == 'bottom_left':
            # go to bottom_right
            coord_opposite = Vector2(bottom_right[1].x / 2 + (entity_size.x / 4),
                                     bottom_right[1].y / 2)
        elif position == 'bottom_right':
            # go to bottom_left
            coord_opposite = Vector2(bottom_left[1].x / 2 - (entity_size.x / 2),
                                     bottom_left[1].y / 2)
        else:  # default : bottom_right
            # go to bottom_left
            coord_opposite = Vector2(bottom_left[1].x / 2 - (entity_size.x / 2),
                                     bottom_left[1].y / 2)
        return coord_opposite
