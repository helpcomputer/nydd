
import pyxel

import constants

class ActorProgressBar:
    def __init__(self, defin):
        self.parent = defin["parent"]
        self.world = defin["world"]
        self.x = 0
        self.y = 0
        self.max_size = defin.get("max_size", [32,8])
        self.value = defin.get("value", 0)
        self.max_value = defin["max_value"]
        self.bar_col = defin.get("bar_col", 8)
        self.bg_col = defin.get("bg_col", 1)
        self.update_func = defin["update_func"]
        self.visible_time = 0

    def update(self):
        self.update_func(self)
        if self.visible_time != -1:
            self.visible_time = max(0, self.visible_time - 1)

    def draw(self):
        if self.visible_time == 0:
            return

        cam = self.world.map.cam
        self.x = self.parent.sprite.position[0] - cam.rect.x
        self.y = (self.parent.sprite.position[1]
            - self.max_size[1]
            - cam.rect.y
            + constants.HUD_H
            - 1)

        pyxel.rect(
            self.x,
            self.y,
            self.max_size[0],
            self.max_size[1],
            self.bg_col
        )
        bar_w = (self.value / self.max_value) * self.max_size[0]
        pyxel.rect(
            self.x,
            self.y,
            bar_w,
            self.max_size[1],
            self.bar_col
        )
