
import pyxel

import constants
import state_stack
import main_menu_state
import input
import utils

g_debug = False

class App:
    def __init__(self):
        pyxel.init(
            constants.SCREEN_W, 
            constants.SCREEN_H, 
            constants.TITLE, 
            constants.FPS, 
            display_scale=3, 
            capture_scale=1,
            capture_sec=20
        )
        pyxel.load("assets/res.pyxres")
        pyxel.image(0).load(0,0,"assets/img00.png")
        utils.load_csv_tilemap("assets/map00.csv", 0)

        self.input = input.Input()

        self.stack = state_stack.StateStack()
        self.stack.push(main_menu_state.MainMenuState({
            "stack" : self.stack,
            "inputs" : self.input,
        }))

        #pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.input.update()

        if pyxel.btnp(pyxel.KEY_F1):
            global g_debug
            g_debug = not g_debug

        self.stack.update(self.input)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.stack.draw()


App()
