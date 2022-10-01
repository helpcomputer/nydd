
import pyxel

import constants
import state_stack
import main_menu_state
import input
import utils
import actor_spawn_tiles

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

        self._load_resources()

        self.input = input.Input()

        self.stack = state_stack.StateStack()
        self.stack.push(main_menu_state.MainMenuState({
            "stack" : self.stack,
            "inputs" : self.input,
        }))

        #pyxel.mouse(True)

        pyxel.run(self.update, self.draw)

    def _load_resources(self):
        pyxel.load("assets/res.pyxres")
        
        pyxel.image(
            constants.IMAGE_BANK_TILES
        ).load(0,0,constants.IMAGE_FILE_TILES)
        pyxel.image(
            constants.IMAGE_BANK_SPRITES
        ).load(0,0,constants.IMAGE_FILE_SPRITES)
        pyxel.image(
            constants.IMAGE_BANK_GUI
        ).load(0,0,constants.IMAGE_FILE_GUI)

        utils.load_csv_tilemap(
            constants.TILEMAP_FILE_TILES,
            constants.TILEMAP_WORLD_TILES
        )
        utils.load_csv_tilemap(
            constants.TILEMAP_FILE_SPAWNS,
            constants.TILEMAP_WORLD_SPAWNS
        )
        actor_spawn_tiles.load_spawns(constants.TILEMAP_WORLD_SPAWNS)

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
