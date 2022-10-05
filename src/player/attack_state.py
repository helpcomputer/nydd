
import pyxel

import constants
import state
import rect

# TODO: Hitbox size to change based on weapon equipped.
HITBOX_SIZE = 8

class Attack(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "attack"
        self.state_machine = state_machine
        self.world = world
        self.player = player

    def enter(self, enter_params=None):
        self.player.sprite.set_state("attack")

    def exit(self):
        pass

    def handle_input(self, inputs):
        move_x = 0
        if inputs.pressing("left"):
            move_x += -1

        if inputs.pressing("right"):
            move_x += 1

        self.player.vel_x = move_x * self.player.run_speed

    def get_hit_rect(self):
        x = self.player.sprite.position[0]
        y = self.player.sprite.position[1]
        if self.player.sprite.flip_h:
            x -= HITBOX_SIZE
        else:
            x += self.player.sprite.size[0]
        return rect.Rect(x, y, HITBOX_SIZE, HITBOX_SIZE)

    def update(self):
        if self.player.sprite.anim_finished:
            if self.player.is_falling:
                self.state_machine.change("fall")
            else:
                if self.player.vel_x != 0:
                    self.state_machine.change("run")
                else:
                    self.state_machine.change("idle")
            return

        if self.player.sprite.frame == 1:
            rect = self.get_hit_rect()
            params = {
                "hitbox" : rect,
                "damage" : 1
            }
            self.world.player_attacked(params)

    def draw(self):
        p = pyxel

        if self.player.sprite.frame == 1:

            cam = self.world.map.cam
            x = self.player.sprite.position[0] - cam.rect.left
            y = (self.player.sprite.position[1] 
                - cam.rect.top 
                + constants.HUD_H)

            if self.player.sprite.flip_h:
                x -= 8
            else:
                x += 16

            p.rect(
                x,
                y,
                8,
                8,
                8
            )
    