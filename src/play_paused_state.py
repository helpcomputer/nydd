
import state
import constants
import utils

class PlayPausedState(state.State):
    def __init__(self, state_machine, params) -> None:
        super().__init__()

        self.state_machine = state_machine
        self.play_state = params["play_state"]
        self.world = params["world"]
        self.hud = params["hud"]

        self.prev_state = None

    def enter(self, prev):
        self.prev_state = prev

    def exit(self):
        self.prev_state = None

    def handle_input(self, inputs):
        if inputs.tapped("button_start"):
            self.state_machine.change(self.prev_state)

    def update(self):
        pass

    def draw(self):
        pstr = "Paused"
        utils.text_label(
            constants.SCREEN_W/2 - utils.get_str_width(pstr)/2,
            constants.SCREEN_H/2,
            pstr
        )
