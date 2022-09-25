
import state
import constants as c
import utils as u

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
        str = "Paused"
        u.text_label(
            c.SCREEN_W/2 - u.get_str_width(str)/2,
            c.SCREEN_H/2,
            str
        )
