from __future__ import annotations
import pygame
from typing import Any
from pygame.math import Vector2

from ...config.constants import *
from ...app import App

class GuiElement(pygame.sprite.Sprite):

    DEFAULT_BLIT_TYPES: tuple = ("surface", "draw")
    DEFAULT_BLIT_TYPE: str = "surface"

    resizing_window_cursors = {'xl': pygame.SYSTEM_CURSOR_SIZEWE,
                                    'xr': pygame.SYSTEM_CURSOR_SIZEWE,
                                    'yt': pygame.SYSTEM_CURSOR_SIZENS,
                                    'yb': pygame.SYSTEM_CURSOR_SIZENS,
                                    'xy': pygame.SYSTEM_CURSOR_SIZENWSE,
                                    'yx': pygame.SYSTEM_CURSOR_SIZENESW
                       }

    def __init__(self,
                 pos: Vector2,
                 size: Vector2,
                 app: App,
                 screen: pygame.Surface,
                 parent: GuiElement = None,
                 settings: dict = None,
                 *args
    ):
        super().__init__(*args)
        self.app: App = app

        self.settings: dict = settings and settings or {}

        self.blit_type: str = settings.get("blit_type", "surface")
        if self.blit_type not in self.DEFAULT_BLIT_TYPES:
            self.blit_type = self.DEFAULT_BLIT_TYPE

        self.background_color: tuple = "background_color" in self.settings and self.settings["background_color"] or \
                                       pygame.Color("white")
        self.border_color: tuple = ()
        self.border_width: int = 0
        self.border_radius: int = 0

        self.register_default_element_values()

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.topleft = pos
        if self.blit_type == "surface":
            self.image.fill(self.background_color)

        self.screen = screen
        self.pos = pos
        self.size = size
        self.parent = parent
        self.children: pygame.sprite.Group = pygame.sprite.Group()

        # font
        self.font_family: str = GUI_STYLES["gui"]["font"]["font_family"]
        self.font_size: int = GUI_STYLES["gui"]["font"]["font_size"]
        self.font_color: tuple = GUI_STYLES["gui"]["font"]["font_color"]
        self.font = pygame.font.SysFont(self.font_family, self.font_size) # todo: move to app level !!!

        # events
        # Note: Event names are analogous and inspired directly by Javascript DOM Api event
        # @docs https://developer.mozilla.org/en-US/docs/Web/Events#event_listing
        self.events: dict = {
            # .... mouse .... #
            'click': [],  # click with moouse
            'mouse_enter': [],  # hover inside element
            'mouse_leave': [],  # hover away from element (make sense it entered first)
            # .... keyboard .... #
            'keydown': [],  # press a keyboard
            'keyup': [],  # release a keyboard
        }
        self.mouse_pointer = pygame.SYSTEM_CURSOR_ARROW
        self.mouse_over: bool = False
        self.mouse_action: str = "NO_ACTION"
        self.element_clicked: bool = False
        self.element_clicked_timer: int = 0

    def update(self, *args, **kwargs):
        # Update self
        self.draw_background()
        self.draw_border()

        # Check events
        self._register_mouse_hover()
        # ****** Mouse Events ****** #
        self._on_mouse_leave()
        self._on_mouse_enter()
        self._on_mouse_click()

        # Update childrens
        self.children.draw(self.screen)
        self.children.update()

    def children_add(self, child: GuiElement) -> None:
        self.children.add(child)

    def draw_background(self) -> None:
        if self.blit_type == "draw":
            pygame.draw.rect(self.image, self.background_color,
                         pygame.Rect(*self.image.get_rect().topleft, *(self.size.x, self.size.y)),
                         border_radius=self.border_radius)

    def draw_border(self) -> None:
        if self.border_color and self.border_width:
            pygame.draw.rect(self.image, self.border_color,
                         pygame.Rect(*self.image.get_rect().topleft, *(self.size.x, self.size.y)),
                         width=self.border_width, border_radius=self.border_radius)

    def surface_clear(self):
        """When do it in a button click it makes a cool effect"""
        self.image.fill(self.background_color)
        self.image.fill((0, 0, 0))

    def register_default_element_values(self):
        """Register to a secondary property a value that may change in time, so by calling
            [prop_name..]_default can have back the initial value

        """

        # hold default values in memory
        self.background_color_default: tuple = self.background_color
        self.border_color_default: tuple = self.border_color
        self.border_width_default: int = self.border_width
        self.border_radius_default: int = self.border_radius

    # -----------------------
    # Events handlers
    # -----------------------

    def add_event_listener(self, event: str, listener: callable) -> Any:
        """Sets up a function that will be called whenever the specified event is delivered to the target.

        Directly insprited by Javascript wep api EventTarget.addEventListener
        @docs https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
        :param event: str A case-sensitive string representing the event type to listen for.
        :param listener: Callable that is called when an event of the specified type occurs.
        :return:
        :raises AttributeError: when event is not in self.events dictionary as key
        """
        if event not in self.events:
            raise AttributeError(f'Event {event} not supported in events list {list(self.events.keys())}')
        # register the event
        self.events[event].append(listener)

    def _register_mouse_hover(self) -> str:
        mouse_leaved = self._is_mouse_leave()
        mouse_entered = False
        if not mouse_leaved:
            mouse_entered = self._is_mouse_enter()
        if mouse_leaved:
            self.mouse_action = "MOUSE_LEAVED"
        elif mouse_entered:
            self.mouse_action = "MOUSE_ENTERED"
        else:
            self.mouse_action = "MOUSE_LEAVED"
        return self.mouse_action

    def _is_mouse_leave(self) -> bool:
        if not self.mouse_over:
            return False
        mouse_position = pygame.mouse.get_pos()
        mouse_collider = pygame.Rect(*mouse_position, 1, 1)
        collision = self.rect.colliderect(mouse_collider)
        if collision:
            return False

        self.mouse_over = False
        return True

    def _is_mouse_enter(self) -> bool:
        mouse_position = pygame.mouse.get_pos()
        mouse_collider = pygame.Rect(*mouse_position, 1, 1)
        collision = self.rect.colliderect(mouse_collider)
        if not collision:
            return False
        self.mouse_over = True
        return True

    def _on_mouse_enter(self) -> None:
        """@ovverride"""
        if self.mouse_action != "MOUSE_ENTERED":
            return
        pygame.mouse.set_cursor(self.mouse_pointer)

        events = self.events['mouse_enter']
        for event in events:
            event()

    def _on_mouse_leave(self) -> None:
        """@ovverride"""
        if self.mouse_action != "MOUSE_LEAVED":
            return
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        events = self.events['mouse_leave']
        for event in events:
            event()

    def _on_mouse_click(self) -> None:
        """@ovverride"""
        if self.mouse_action != "MOUSE_ENTERED":
            return
        # Did the user click ? TODO: make event for each mouse button? or should be 'callable' that checks that?
        app_events = self.app.event_listener.events
        event_click = app_events.get(pygame.MOUSEBUTTONDOWN, {})
        if not event_click:  # if empty, then user did not click
            return

        events = self.events['click']
        for event in events:
            event(event_click) # call callbacks
