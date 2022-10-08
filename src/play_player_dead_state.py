
import pyxel

import state
import utils
import constants
import main_menu_state

EXIT_DELAY = 3
DRAMATIC_PAUSE = 0.25

class PlayPlayerDeadState(state.State):
    def __init__(self, state_machine, params) -> None:
        super().__init__()

        self.state_machine = state_machine
        self.play_state = params["play_state"]
        self.world = params["world"]
        self.hud = params["hud"]

        self.exit_delay = EXIT_DELAY
        self.dramatic_pause = DRAMATIC_PAUSE

    def enter(self, enter_params=None):
        pass

    def exit(self):
        self.stack.push(main_menu_state.MainMenuState({
            "stack" : self.stack,
        }))

    def handle_input(self, inputs):
        if self.exit_delay == 0:
            if inputs.tapped("button_start"):
                self.play_state.stack.pop()
                return

    def update(self):
        if self.exit_delay > 0:
            self.exit_delay = max(
                0, 
                self.exit_delay - constants.SECS_PER_FRAME
            )

        if self.dramatic_pause > 0:
            self.dramatic_pause = max(
                0, 
                self.dramatic_pause - constants.SECS_PER_FRAME
            )
        else:
            self.world.update()
            self.hud.update()

    def draw(self):
        text = "Game Over"
        utils.text(
            constants.SCREEN_W/2 - utils.get_str_width(text)/2,
            constants.SCREEN_H/3,
            text,
            pyxel.COLOR_RED
        )

        if self.exit_delay == 0:
            text = "Press Start"
            utils.text(
                constants.SCREEN_W/2 - utils.get_str_width(text)/2,
                constants.SCREEN_H/3 * 2,
                text,
                pyxel.COLOR_WHITE
            )
