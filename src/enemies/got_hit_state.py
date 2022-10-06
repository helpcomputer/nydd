
import pyxel

import state
import actor
import constants

TIMEOUT = 0.2
PUSH_BACK_SPEED = 1

class GotHit(state.State):
    def __init__(self, enemy_self, state_machine, world) -> None:
        super().__init__()
        self.name = "got_hit"
        self.state_machine = state_machine
        self.world = world
        self.enemy_self = enemy_self

        self.return_state = None
        self.return_params = {}
        self.timeout_timer = 0

    def enter(self, params):
        self.return_state = params["return_state"]
        self.timeout_timer = 0

        self.enemy_self.update_func = self.update
        self.enemy_self.draw_func = self.draw
        self.enemy_self.set_flip_func = actor.empty_callback
        self.enemy_self.sprite.anim_paused = True

        if params["hit_from"] == "left":
            self.enemy_self.vel_x = PUSH_BACK_SPEED
        else:
            self.enemy_self.vel_x = -PUSH_BACK_SPEED

    def exit(self):
        self.enemy_self.update_func = self.enemy_self.default_update
        self.enemy_self.draw_func = self.enemy_self.default_draw
        self.enemy_self.set_flip_func = None
        self.enemy_self.sprite.anim_paused = False

    def handle_input(self, inputs):
        pass

    def update(self):
        actor.Actor.update(self.enemy_self)
        self.enemy_self.keep_on_screen()
        self.enemy_self.set_flip()

        self.timeout_timer += constants.SECS_PER_FRAME
        if self.timeout_timer >= TIMEOUT:
            self.state_machine.change(self.return_state, self.return_params)

    def draw(self):
        for c in range(pyxel.NUM_COLORS):
            pyxel.pal(c, pyxel.COLOR_WHITE)
        self.enemy_self.sprite.draw(self.world.map.cam)
        pyxel.pal()
