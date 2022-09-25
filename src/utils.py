
import csv

import pyxel as p

def text(x, y, str, col=7, shadow=1):
    p.text(x, y+1, str, shadow)
    p.text(x, y, str, col)

def text_label(x, y, str, col=7, shadow=1, bg_col=0):
    p.rect(
        x,
        y,
        get_str_width(str),
        p.FONT_HEIGHT,
        bg_col
    )
    text(x, y, str, col, shadow)

def get_str_width(str):
    return len(str) * p.FONT_WIDTH

def load_csv_tilemap(file, tm_num, posX=0, posY=0):
    tiles_per_image_row = p.IMAGE_SIZE // p.TILE_SIZE
    data = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            line = []
            for item in row:
                n = int(item)
                x = n % tiles_per_image_row
                y = n // tiles_per_image_row
                str = format(x,'02x') + format(y,'02x')
                line.append(str)
            data.append(line)

    res = []
    for y in range(len(data)):
        res.append(' '.join(data[y]))

    p.tilemap(tm_num).set(posX, posY, res)
