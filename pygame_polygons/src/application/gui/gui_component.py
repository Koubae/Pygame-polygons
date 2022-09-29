import pygame
from typing import Optional, Any
from pygame.math import Vector2
from ..views import ViewManager
from . import GuiPanel, GuiButton


class GuiComponent:
    DEFAULT_WINDOW_BACKGROUND_COLOR: tuple[int, int, int, int] = (51, 206, 255, 55)
    DEFAULT_WINDOW_SIZE: Vector2 = Vector2(500, 350)

    DEFAULT_BTN_CLOSE_BACKGROUND_COLOR: tuple[int, int, int] = (224, 224, 224)
    DEFAULT_BTN_CLOSE_BORDER_COLOR: tuple[int, int, int] = (224, 224, 224)

    def __init__(self, app, view, *_, **__):
        self.app = app
        self.screen: pygame.Surface = app.background
        self.view: ViewManager = view
        self.gui_group = pygame.sprite.Group()

        # Note: override these class properties to change the button close component
        # because in general, a pop-up or component may always kind of look the same, this saves tons
        # of boiler plate code. off course, UI component are infinite, so in case, just split the class in more
        # sub-cluses with more fain-grained behaviour!

        self.window_size: Vector2 = self.DEFAULT_WINDOW_SIZE
        self.window: GuiPanel = GuiPanel(
            Vector2(self.app.win_width * 2, self.app.win_width * 2), # makes sure is out of the view!
            self.window_size,
            self.app,
            self.app.background,
            None,
            {
                'background_color': self.DEFAULT_WINDOW_BACKGROUND_COLOR
            }
        )
        self.gui_group.add(self.window)

        # Create close button of the component

        self.btn_window_close_size: Vector2 = Vector2(35, 25)
        self.btn_window_close: GuiButton = GuiButton("X", Vector2((self.window_size.x - 50), 10),
                                          self.btn_window_close_size,
                                          self.app, self.window.image,
                                          self.window, {
                                              'background_color': self.DEFAULT_BTN_CLOSE_BACKGROUND_COLOR,
                                              'border_color': self.DEFAULT_BTN_CLOSE_BORDER_COLOR
                                          })
        self.gui_group.add(self.btn_window_close)
        self.window.children_add(self.btn_window_close)
        self.btn_window_close.add_event_listener("click", self.close_component)

        self.window_position: Vector2 = Vector2(0, 0)
        self.btn_window_close_position: Vector2 = Vector2(self.window_size.x - self.btn_window_close_size.x * 2,
                                                          self.btn_window_close_size.y + 15)

    def render(self, context_center: Optional[Vector2], *_, **__) -> None:
        """Render the component

        :param context_center: Vector2|None If provided, will render the component on the opposite side of the x,y coodinates
        :param _:
        :param __:
        :return:
        """
        if context_center:
            self._calculate_new_component_position(context_center)
        self._pre_render(*_, **__)
        self._render()

    def _render(self):
        self._draw_component_default_guis()
        # Update Gui Components
        self.gui_group.draw(self.screen)
        self.gui_group.update()

    def _pre_render(self, *args: Any, **kwargs: Any) -> Any:
        """Child classes shoudl define render logic here
        @mustoverride
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def _clean_up(self, *args, **kwargs):
        """@mustovverride
            Perform various clean-ups of the component
        """
        pass


    def _calculate_new_component_position(self, context_center: Vector2) -> None:

        # now we need to determine the position of the center of the polygon, Is it in the
        # we devide the screen in 4 (TOP-LEFT, TOP-RIGHT, BOTTOM-LEFT, BOTTOM-RIGHT)
        # add set to opposite direction
        # now, we make the position of the window setting the opposite of the selected coordinates
        setting_window_position: Optional[Vector2] = self.app.get_window_opposite_position(
            context_center,
            self.window_size
        )
        if not setting_window_position:
            return
            # move context polygon setting window
        self.window_position = setting_window_position
        self.btn_window_close_position = Vector2(
            self.window_size.x + (
                    abs(setting_window_position.x) - (abs(self.btn_window_close_size.x) * 2)),
            abs(self.btn_window_close_size.y + setting_window_position.y)
        )

    def _draw_component_default_guis(self) -> None:
        """Draws to screen the default component default guis"""
        self.window.move_gui_into(self.window_position)
        self.btn_window_close.move_gui_into(self.btn_window_close_position)

    def close_component(self, event: dict) -> None:
        """Closes / Resets a component """
        if 'MOUSE_LEFT' not in event:
            return
        self.view.mode = self.view.VIEW_MODES[0]
        self._clean_up()
