import pygame

# pygame constants
CLOCK = pygame.time.Clock()
FRAMES: int = 60

# world
display_info = pygame.display.Info()
DISPLAY_WIDTH: int = display_info.current_w
DISPLAY_HEIGHT: int = display_info.current_h

FLOOR_CHUNK: int = 64
SCREEN_SIZE: list = ["small", "medium", "large"]
SCREEN_SELECT: str = SCREEN_SIZE[2]
SCREEN_SIZE_CALCS: list = ["static", "dynamic"]  # static: fix number | dynamic : calcualtes from the pc display size
SCREEN_SIZE_TYPE: str = SCREEN_SIZE_CALCS[1]
if SCREEN_SIZE_TYPE == "static":
    if SCREEN_SELECT == "large":
        WIN_WIDTH = FLOOR_CHUNK * 30  # 1920
        WIN_HEIGHT = int(FLOOR_CHUNK * 16.875)  # 1080
    elif SCREEN_SELECT == "medium":
        WIN_WIDTH = FLOOR_CHUNK * 20  # 1280
        WIN_HEIGHT = FLOOR_CHUNK * 10  # 640
    else:  # Small
        WIN_WIDTH = FLOOR_CHUNK * 10  # 640
        WIN_HEIGHT = FLOOR_CHUNK * 5  # 320
else:
    if SCREEN_SELECT == "large":
        WIN_WIDTH = DISPLAY_WIDTH - 0
        WIN_HEIGHT = DISPLAY_HEIGHT - 0
        FLOOR_CHUNK = int(WIN_WIDTH / 30)  # at best should be 64
    elif SCREEN_SELECT == "medium":
        WIN_WIDTH = int(DISPLAY_WIDTH / 1.5)
        WIN_HEIGHT = int(DISPLAY_HEIGHT / 1.5)
        FLOOR_CHUNK = int(WIN_WIDTH / 20)
    else:  # Small
        WIN_WIDTH = int(DISPLAY_WIDTH / 3)
        WIN_HEIGHT = int(DISPLAY_HEIGHT / 3.375)
        FLOOR_CHUNK = int(WIN_WIDTH / 10)

# ensure no decimal in the screen size
WIN_WIDTH: int = int(WIN_WIDTH)
WIN_HEIGHT: int = int(WIN_HEIGHT)
FLOOR_CHUNK: int = int(FLOOR_CHUNK)

WIN_SIZE: tuple = (WIN_WIDTH, WIN_HEIGHT)
# inputs
MOUSE_BUTTON_MAP: dict = {
    1: 'MOUSE_LEFT',
    2: 'MOUSE_CENTRAL',
    3: 'MOUSE_RIGHT',
    4: 'WHEEL_UP',
    5: 'WHEEL_DOWN'
}

MOUSE_WHEEL: dict = {
    -1: 'WHEEL_DOWN',
    1: 'WHEEL_UP'
}


# Settings
GUI_STYLES: dict = { # todo: make a json setting????

    'gui': {
        'font': {
            'font_family': 'ariel',
            'font_size': 18,
            'font_color': (190, 0, 150)
        },
        'panel': {
            'background_color': (120, 0, 150, 55),
            'border_color': (120, 0, 150),
            'border_width': 2,
            'border_radius': 5,
        },
        'button': {
            'background_color': (102, 255, 178),
            'border_color': (0, 204, 102),
            'border_width': 3,
            'border_radius': 10,
        }
    }
}
