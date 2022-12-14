
import pyxel as p

import constants
import progress_bar
import utils

HP_BAR_MIN_WIDTH = 12
MP_BAR_MIN_WIDTH = 12
HP_BAR_MAX_WIDTH = 52
MP_BAR_MAP_WIDTH = 52
BAR_HEIGHT = 5

class Hud():
    def __init__(self, theWorld):
        self.world = theWorld
        self.player = theWorld.player
        self.health_bar = progress_bar.ProgressBar({
            "x" : 8,
            "y" : 1,
            "max_size" : [HP_BAR_MIN_WIDTH, BAR_HEIGHT],
            "value" : 0,
            "max_value" : 0,
            "bar_col" : 8,
        })
        self.magic_bar = progress_bar.ProgressBar({
            "x" : 8,
            "y" : 9,
            "max_size" : [MP_BAR_MIN_WIDTH, BAR_HEIGHT],
            "value" : 0,
            "max_value" : 0,
            "bar_col" : 3,
        })
        self.gold = 0
        self.crystals = 0

        self.update()

    def update(self):
        self.health_bar.value = self.player.stats.get("hp_now")
        self.health_bar.max_value = self.player.stats.get("hp_max")
        self.magic_bar.value = self.player.stats.get("mp_now")
        self.magic_bar.max_value = self.player.stats.get("mp_max")
        self.gold = self.world.gold
        self.crystals = self.world.crystals

    def draw(self):
        # BG
        p.rect(
            0, 0, constants.SCREEN_W, 16, 
            p.COLOR_BLACK
        )

        # Life
        p.blt(
            0,0,
            constants.IMAGE_BANK_GUI,
            0,248,8,8,
            p.COLOR_BLACK
        )
        self.health_bar.draw()
        # Magic
        p.blt(
            0,8,
            constants.IMAGE_BANK_GUI,
            8,248,8,8,
            p.COLOR_BLACK
        )
        self.magic_bar.draw()
        # Gold
        p.blt(
            constants.SCREEN_W/2,0,
            constants.IMAGE_BANK_GUI,
            16,248,8,8,
            p.COLOR_BLACK
        )
        utils.text(
            constants.SCREEN_W/2+8, 
            1, 
            "{:08}".format(self.gold), 
            p.COLOR_WHITE
        )
        # Crystals
        p.blt(
            constants.SCREEN_W/2,
            8,
            constants.IMAGE_BANK_GUI,
            8,240,8,8,
            p.COLOR_BLACK
        )
        utils.text(
            constants.SCREEN_W/2+8, 
            9, 
            "{}".format(self.crystals), 
            p.COLOR_WHITE
        )
        # Weapon
        p.blt(
            constants.SCREEN_W-20,0,
            constants.IMAGE_BANK_GUI,
            24,240,16,16,
            p.COLOR_BLACK
        )
