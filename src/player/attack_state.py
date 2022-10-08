
import pyxel

import constants
import state
import rect
import app

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

    def get_attack_box(self):
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
            rect = self.get_attack_box()
            attacker_cen_x = (self.player.sprite.position[0] 
                + self.player.hitbox.mid_x)
            params = {
                "attacker_cen_x" : attacker_cen_x,
                "hitbox" : rect,
                "damage" : 1
            }
            self.world.player_attacked(params)

    def draw(self):
        if app.g_debug:
            cam = self.world.map.cam
            ab = self.get_attack_box()
            ab.x -= cam.rect.left
            ab.y -= cam.rect.top - constants.HUD_H
            ab.draw(pyxel.COLOR_WHITE)
    