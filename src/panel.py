
import pyxel

import constants

class Panel:
    def __init__(self, paras=None):
        params = paras or {}
        self.img_num = params.get("img_num", constants.IMAGE_BANK_GUI)
        self.nine_patch_pos = params.get("nine_patch_pos", (44,244))
        self.tile_size = params.get("tile_size", 4)
        self.nine_tiles = []
        self.panel_tiles = [] # [ [tileIndex, x, y, w, h], ...]

        # Create a uv list [u,v] for each tile.
        # tile 0 = top left
        # tile 1 = top
        # tile 2 = top right
        # tile 3 = left
        # tile 4 = middle
        # tile 5 = right
        # tile 6 = bottom left
        # tile 7 = bottom
        # tile 8 = bottom right
        for y in range(3):
            for x in range(3):
                self.nine_tiles.append([
                    self.nine_patch_pos[0] + x * self.tile_size, 
                    self.nine_patch_pos[1] + y * self.tile_size
                ])

    def get_position(self):
        return (self.panel_tiles[0][1], self.panel_tiles[0][2])
            
    def set_position(self, x, y, width_tiles, height_tiles):
        self.panel_tiles = [] # clear list
        
        wTiles = max(3, width_tiles)
        hTiles = max(3, height_tiles)
        
        tileIndex = 0
        for yTile in range(hTiles):
            for xTile in range(wTiles):
                if xTile == 0: # left column
                    if yTile == 0:
                        tileIndex = 0
                    elif yTile == hTiles -1:
                        tileIndex = 6
                    else:
                        tileIndex = 3
                elif xTile == wTiles - 1: # right column
                    if yTile == 0:
                        tileIndex = 2
                    elif yTile == hTiles -1:
                        tileIndex = 8
                    else:
                        tileIndex = 5
                else: # middle column
                    if yTile == 0:
                        tileIndex = 1
                    elif yTile == hTiles -1:
                        tileIndex = 7
                    else:
                        tileIndex = 4
            
                self.panel_tiles.append([
                    tileIndex, 
                    x + xTile * self.tile_size, 
                    y + yTile * self.tile_size
                ])
                
    def set_position_centre(self, x, y, width_tiles, height_tiles):
        hWidth = width_tiles // 2
        hHeight = height_tiles // 2
        self.set_position(
            x - hWidth * self.tile_size, 
            y - hHeight * self.tile_size,
            width_tiles,
            height_tiles
        )
        
    def draw(self):
        for tile in self.panel_tiles:
            pyxel.blt(
                tile[1], tile[2], self.img_num, 
                self.nine_tiles[tile[0]][0], 
                self.nine_tiles[tile[0]][1],
                self.tile_size, self.tile_size,
            )
        
        
        
        
        