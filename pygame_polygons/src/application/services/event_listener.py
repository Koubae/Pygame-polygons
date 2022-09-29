import pygame
from typing import Optional, Any
from ...config.constants import MOUSE_BUTTON_MAP, MOUSE_WHEEL


class EventListener:

    def __init__(self, app):
        self.app = app
        self.events: dict = {}
        self.element_hovered: Optional[Any] = None

    def events_new(self) -> None:
        """Clear the events container"""
        self.events.clear()

    def events_listen(self):
        """Register the events
            NOTE: we could do, as an approach to listen to ALL events and not arbitrarly
            add if - else statemens for target events
        """
        self.events_new()
        for event in pygame.event.get():
            try:

                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):  # x button and esc terminates the game!
                    self.app.switch_off()
                    return
                if event.type not in self.events:
                    self.events[event.type] = {}

                # ............. Mouse ............. #
                if event.type == pygame.MOUSEBUTTONDOWN:
                    try:
                        self.events[event.type][MOUSE_BUTTON_MAP[event.button]] = True
                    except KeyError:
                        pass
                if event.type == pygame.MOUSEBUTTONUP:
                    self.events[event.type][MOUSE_BUTTON_MAP[event.button]] = True
                if event.type == pygame.MOUSEWHEEL:
                    self.events[event.type][MOUSE_WHEEL[event.y]] = True
                # ............. Keyboard ............. #
                if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                    self.events[event.type][event.key] = True
            except KeyError:
                continue

    # ---------------------------
    # Event utiliy and api
    # ---------------------------

    def event_get_mouse_wheel(self) -> Optional[str]:
        """Returns the wheel action or None if no wheel action currently is fired

        :return: str|None
        """
        if not self.is_mouse_wheel_event():
            return None
        action = self.events[pygame.MOUSEWHEEL]
        if 'WHEEL_UP' in action:
            return 'WHEEL_UP'
        elif 'WHEEL_DOWN' in action:
            return 'WHEEL_DOWN'
        return None

    # ~~~~~~~~~~~~~~~~~ mouse ~~~~~~~~~~~~~~~~~ #
    def is_mouse_button_pressed_event(self) -> bool:
        return pygame.MOUSEBUTTONDOWN in self.events

    def is_mouse_button_released_event(self) -> bool:
        return pygame.MOUSEBUTTONUP in self.events

    def is_mouse_wheel_event(self) -> bool:
        return pygame.MOUSEWHEEL in self.events

    # ~~~~~~~~~~~~~~~~~ keyboard ~~~~~~~~~~~~~~~~~ #

    def is_ctrl_left_pressed_event(self) -> bool:
        return pygame.KEYDOWN in self.events and pygame.K_LCTRL in self.events[pygame.KEYDOWN]

    def is_ctrl_left_released_event(self) -> bool:
        return pygame.KEYUP in self.events and pygame.K_LCTRL in self.events[pygame.KEYUP]