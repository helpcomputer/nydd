
import pyxel

import constants

INDEX = {
    988 : "player",
    984 : "old_lady",
    920 : "octoman",
}

# g_spawns = {
#     screen_index : {
#         tile_index : actor_name
#     },
#    "player" : tile_index
# }
g_spawns = {}

def load_spawns(tm_num):
    c = constants

    for ty in range(pyxel.TILEMAP_SIZE):
        for tx in range(pyxel.TILEMAP_SIZE):
            tile = pyxel.tilemap(tm_num).pget(tx, ty)
            img_tile_index = tile[0]+tile[1]*c.TILE_IMAGE_TILES_WIDE
            name = INDEX.get(img_tile_index)
            if name:
                if name == "player":
                    assert(g_spawns.get(name) is None)
                    tm_tile_index = tx + ty * c.TILEMAP_TILES_WIDE
                    g_spawns[name] = tm_tile_index
                else:
                    screen_x = tx * 8 // c.SCREEN_W
                    screen_y = ty * 8 // c.VIEW_H
                    scr_index = screen_x + screen_y * c.TILEMAP_SCREENS_WIDE
                    scr_dict = g_spawns.get(scr_index)
                    if not scr_dict:
                        scr_dict = g_spawns[scr_index] = {}
                    tm_tile_index = tx + ty * c.TILEMAP_TILES_WIDE
                    assert(scr_dict.get(tm_tile_index) is None)
                    scr_dict[tm_tile_index] = name

    print(g_spawns)
