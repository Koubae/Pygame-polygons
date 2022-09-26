import sys

from .app import App
from .config.constants import *
# from .application.views.Vi import ViewHome
# from .application.views import ViewHome
from .application.views import Views

class AppRunner:

    def __init__(self): ...

    def on(self):

        # pygame setup
        app = App(
            "Drawings",
            {
                'clock': CLOCK,
                'frames': FRAMES
            },
            {
                'display_info': display_info,
                'screen_size': SCREEN_SELECT,
                'screen_size_type': SCREEN_SIZE_TYPE,
                'display_width': DISPLAY_WIDTH,
                'display_height': DISPLAY_HEIGHT,

                'win_size': WIN_SIZE,
                'win_width': WIN_WIDTH,
                'win_height': WIN_HEIGHT,
                'chunk': FLOOR_CHUNK,
            })

        views = Views(app)
        views.game_beat()

        # at this point we close the app!
        pygame.quit()
        sys.exit(0)



