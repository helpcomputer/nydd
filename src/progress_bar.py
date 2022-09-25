
import pyxel as p

class ProgressBar:
    def __init__(self, defin):
        self.x = defin["x"]
        self.y = defin["y"]
        self.max_size = defin.get("max_size", [32,8])
        self.value = defin.get("value", 0)
        self.max_value = defin["max_value"]

        self.bar_col = defin.get("bar_col", 8)
        self.outline_col = defin.get("outline_col", 7)

    def draw(self):
        bar_w = (self.value / self.max_value) * self.max_size[0]-2
        p.rect(
            self.x+1,
            self.y+2,
            bar_w,
            self.max_size[1]-3,
            self.bar_col
        )
        p.rectb(
            self.x,
            self.y,
            self.max_size[0],
            self.max_size[1],
            self.outline_col
        )
