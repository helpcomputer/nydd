
import pyxel as p

CONFIG = {
    "up" : p.KEY_UP,
    "down" : p.KEY_DOWN,
    "left" : p.KEY_LEFT,
    "right" : p.KEY_RIGHT,
    "button_attack" : p.KEY_Z,
    "button_jump" : p.KEY_X,
    "button_start" : p.KEY_RETURN,
}

class Input:
    def __init__(self) -> None:
        self._tapped = {}
        self._pressing = {}

    def pressing(self, k_name):
        return self._pressing.get(k_name)

    def tapped(self, k_name):
        return self._tapped.get(k_name)

    def update(self):
        for k in CONFIG.keys():
            self._pressing[k] = p.btn(CONFIG[k])
            self._tapped[k] = p.btnp(CONFIG[k])
