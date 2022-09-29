from typing import Optional
import pygame


class Slider:
    """Component representation of a range slider
        For webDev!!  is like a input range <input type="range" />
            -> https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/range

    """

    def __init__(self, x, y, w, h):
        h = h + 5
        self.rad = h // 2
        self.pwidth = w - self.rad * 2
        self.rect = pygame.Rect(x, y, self.pwidth + 12, h)
        self.image = pygame.Surface((self.pwidth + 12, h), flags=pygame.SRCALPHA)
        SEE_BOX: bool = False
        if SEE_BOX:
            # use it to better see the actual size of the surface , however most of cases is better leave it off
            # because is tremendously ugly!
            self.image.fill((255, 255, 255))

        color = pygame.Color("white")

        self.slide_value: int = 1
        self.slide_mapping: dict = {}
        for i in range(self.pwidth):
            width = i + self.rad
            self.slide_mapping[width] = i
            pygame.draw.rect(self.image, color, (width, 2, 1, h - 5))
        self.p = 0

    def get_slider_value(self) -> int:
        """
        Get the current slide value
        :return: int
        """
        pos = int(self.rad + self.p * self.pwidth)

        value: Optional[int] = None
        total_values = len(self.slide_mapping)
        count = 0
        while count < total_values:
            try:
                value = self.slide_mapping[pos]
                if value:
                    break
            except KeyError:
                pass

            count += 1
            pos += 1
        if value is None:  # grap last value
            value = list(self.slide_mapping)[-1]
        value = max(1, value)
        self.slide_value = value
        return value

    def update(self):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))
            print(self.p)

        self.get_slider_value()

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, pygame.Color("black"), center, self.rect.height // 2)
