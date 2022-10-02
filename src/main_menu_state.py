
import pyxel

import state
import play_state
import utils
import constants
import text_box

class MainMenuState(state.State):
    def __init__(self, params) -> None:
        super().__init__()

        self.stack = params["stack"]

        self.degrees = 0

    def enter(self):
        pass

    def exit(self):
        self.stack.push(play_state.PlayState({
            "stack" : self.stack,
        }))

        text = (
            "You awaken on the floor with a headache. You are in a "
            "cold, dank, wet room. You hear strange noises in the distance,"
            " you must escape this place. You must find a way out..."
        )
        self.stack.push(
            text_box.TextBox({
                "stack" : self.stack,
                "text" : text,
            })
        )

    def handle_input(self, inputs):
        if inputs.tapped("button_start"):
            self.stack.pop()

    def update(self):
        self.degrees += 3
        if self.degrees >= 360:
            self.degrees -= 360

    def draw(self):
        c = constants
        u = utils
        # Title bg
        pyxel.blt(
            0,0,
            c.IMAGE_BANK_GUI,
            0,0,c.SCREEN_W, c.SCREEN_H
        )
        # Titles
        pyxel.blt(
            33,40 + pyxel.sin(self.degrees)*2,
            c.IMAGE_BANK_GUI,
            128,0,62,18,
            pyxel.COLOR_BLACK
        )

        if self.degrees < 180:
            start_game = "Press Start"
            u.text(
                c.SCREEN_W/2 - u.get_str_width(start_game)/2,
                88,
                start_game,
            )
    