
import state
import play_state
import utils
import constants

class MainMenuState(state.State):
    def __init__(self, params) -> None:
        super().__init__()

        self.stack = params["stack"]

    def enter(self):
        pass

    def exit(self):
        self.stack.push(play_state.PlayState({
            "stack" : self.stack,
        }))

    def handle_input(self, inputs):
        if inputs.tapped("button_start"):
            self.stack.pop()

    def update(self):
        pass

    def draw(self):
        c = constants
        u = utils
        welcome_text = "Welcome to Nydd"
        u.text(
            c.SCREEN_W/2 - u.get_str_width(welcome_text)/2,
            c.SCREEN_H/3,
            welcome_text,
            8
        )
        start_game = "Press Enter to Start"
        u.text(
            c.SCREEN_W/2 - u.get_str_width(start_game)/2,
            c.SCREEN_H/3 * 2,
            start_game,
        )
    