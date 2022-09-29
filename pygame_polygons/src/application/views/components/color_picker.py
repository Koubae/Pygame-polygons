import pygame

class ColorPicker:
    """Color Picker Bar
        @credit:
            - StackOverflow
            - User @Rabbid76 https://stackoverflow.com/users/5577765/rabbid76
            - Answer: https://stackoverflow.com/a/73518042/13903942
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

        self.current_color = None
        self.c_m = {}
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360 * i / self.pwidth), 100, 50, 100)
            width = i + self.rad
            self.c_m[width] = color
            pygame.draw.rect(self.image, color, (width, 2, 1, h - 5))
        self.p = 0

    def get_color(self):
        """
        Get the current picker Color
        :return:
        """
        pos = int(self.rad + self.p * self.pwidth)

        color = None
        total_colors = len(self.c_m)
        count = 0
        while count < total_colors:
            try:
                color = self.c_m[pos]
                if color:
                    break
            except KeyError:
                pass

            count += 1
            pos += 1
        if not color:
            color = pygame.Color(0)
        self.current_color = color
        return color

    def update(self):
        moude_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

    def draw(self, surf):
        surf.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pygame.draw.circle(surf, self.get_color(), center, self.rect.height // 2)
