
import pyxel

import state
import constants

TIMEOUT = 0.2
PUSH_BACK_SPEED = 1.5
PUSH_UP_SPEED = 4

class GotHit(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "got_hit"
        self.state_machine = state_machine
        self.world = world
        self.player = player

        self.timeout_timer = 0
        self.flash_draw = False

    def enter(self, params):
        self.player.sprite.set_state(self.name)
        self.timeout_timer = 0
        self.player.vel_x = PUSH_BACK_SPEED
        self.player.vel_y = -PUSH_UP_SPEED
        self.player.sprite.flip_h = True
        if params["hit_from"] == "right":
            self.player.vel_x = -PUSH_BACK_SPEED
            self.player.sprite.flip_h = False

    def exit(self):
        pass

    def handle_input(self, inputs):
        pass

    def update(self):
        self.timeout_timer += constants.SECS_PER_FRAME
        if self.timeout_timer >= TIMEOUT:
            self.state_machine.change("fall")

    def draw(self):
        pass
