
import pyxel as p

import constants as c
import camera

SOLID_TILE_Y_MAX = 15
ONE_WAY_TILE_ROW = 15

class Map:
    def __init__(self, params) -> None:
        self.world = params["world"]
        self.image_bank = params.get("image_bank", c.IMAGE_BANK_TILES)
        self.tilemap = params["tilemap"]
        self.cam = camera.Camera()

    def is_solid(self, tile_x, tile_y):
        tile = self.get_tile(tile_x, tile_y)
        return tile[1] < SOLID_TILE_Y_MAX

    def is_one_way(self, tile_x, tile_y):
        tile = self.get_tile(tile_x, tile_y)
        return tile[1] == ONE_WAY_TILE_ROW

    def get_tile(self, tile_x, tile_y):
        """Returns a tuple of (tile_x, tile_y)
        as tilemap image indices.
        """
        return p.tilemap(self.tilemap).pget(tile_x, tile_y)

    def update(self):
        pass

    def draw(self):
        p.bltm(
            0,
            c.HUD_H, 
            self.image_bank,
            self.cam.rect.left, 
            self.cam.rect.top, 
            self.cam.rect.w, 
            self.cam.rect.h
        )