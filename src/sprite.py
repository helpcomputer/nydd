
import pyxel as p

import constants

class Sprite:
    def __init__(self, defin, x, y):
        self.position = [x, y]
        self.anims = defin.get("states", None)
        self.image_bank = constants.IMAGE_BANK_SPRITES
        self.colour_key = defin.get("colour_key", p.COLOR_BLACK)
        self.state = defin.get("start_state", "idle")
        if len(self.anims) == 1:
            self.state = next(iter(self.anims))
        self.frame = defin.get("start_frame", 0)
        self.frame_time = 0
        self.flip_h = defin.get("flip_h", False)
        self.flip_v = defin.get("flip_v", False)
        self.size = defin.get("size", (8,8))
        self.visible = defin.get("visible", True)
        self.anim_finished = False
        self.anim_paused = False

    def set_state(self, state):
        if state not in self.anims:
            return

        if state == self.state:
            return

        self.state = state
        self.frame = 0
        self.frame_time = 0
        self.anim_finished = False

    def get_frame_uv(self):
        return self.anims[self.state]["frames"][self.frame]

    def animate(self):
        if self.anim_paused:
            return
        if self.anims:
            self.frame_time += constants.SECS_PER_FRAME
            if self.frame_time >= self.anims[self.state]["frame_spd"]:
                self.frame_time = 0
                self.frame += 1
                if self.frame == len(self.anims[self.state]["frames"]):
                    loop = self.anims[self.state].get("loop")
                    if loop is not None:
                        if loop:
                            self.frame = 0
                        else:
                            self.frame -= 1
                            self.anim_finished = True
                    else:
                        self.frame = 0

    def update(self):
        self.animate()

    def draw(self, camera=None):
        if not self.visible:
            return

        uv = self.get_frame_uv()
        p.blt(
            p.floor(self.position[0] 
                - camera.rect.left), 
            p.floor(self.position[1] 
                - camera.rect.top
                + constants.HUD_H), 
            self.image_bank, 
            uv[0],
            uv[1],
            -self.size[0] if self.flip_h else self.size[0],
            -self.size[1] if self.flip_v else self.size[1],
            self.colour_key
        )
