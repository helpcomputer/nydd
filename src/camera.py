
import constants as c
import rect

class Camera:
    def __init__(self) -> None:
        self.rect = rect.Rect(
            0,
            0,
            c.SCREEN_W,
            c.SCREEN_H - c.HUD_H
        )

    def set_position(self, x, y):
        self.rect.x = (x // self.rect.w) * self.rect.w
        self.rect.y = (y // self.rect.h) * self.rect.h

        #print("set cam to {},{}".format(self.rect.x, self.rect.y))

