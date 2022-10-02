
import pyxel as p

import constants as c
import rect
import sprite
import app
import stats
import actor_defs

GRAVITY = 0.5
MAX_FALL_SPEED = 2.5

class Actor:
    def __init__(self, world, defin, x, y):
        self.type = defin["type"]
        self.world = world
        self.sprite = sprite.Sprite(defin, x, y)
        self.hitbox = rect.Rect(*(defin.get("hitbox", (8,8,8,8))))
        self.vel_x = 0
        self.vel_y = 0
        self.is_falling = False
        self.uid = 0
        self.is_alive = True
        self.stats = stats.Stats(
            actor_defs.BASE_STATS[self.type]
        )

    def get_state(self):
        return self.sprite.state

    def set_state(self, state):
        self.sprite.set_state(state)

    def move(self):
        last_y = self.sprite.position[1]

        sig = p.sgn(self.vel_x)
        if sig < 0:
            self.sprite.flip_h = True
        elif sig > 0:
            self.sprite.flip_h = False

        self.apply_gravity()

        pos = self.sprite.position
        pos[0], pos[1], self.vel_x, self.vel_y = \
            self.push_back(pos[0], pos[1], self.vel_x, self.vel_y)

        self.is_falling = self.sprite.position[1] > last_y

    def apply_gravity(self):
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)

    def detect_collision(self, x, y):
        x1 = int((x + self.hitbox.left) // 8)
        y1 = int((y + self.hitbox.top) // 8)
        x2 = int((x + self.hitbox.right - 1) // 8)
        y2 = int((y + self.hitbox.bottom - 1) // 8)
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                if self.world.map.is_solid(xi, yi):
                    return True
        return False

    def push_back(self, x, y, dx, dy):
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        if abs_dx > abs_dy:

            total_moved_abs = 0
            sign = 1 if dx > 0 else -1
            while total_moved_abs < abs_dx:
                d = min(1, abs_dx - total_moved_abs) * sign
                if self.detect_collision(x + d, y):
                    break
                x += d
                total_moved_abs += abs(d)

            total_moved_abs = 0
            sign = 1 if dy > 0 else -1
            while total_moved_abs < abs_dy:
                d = min(1, abs_dy - total_moved_abs) * sign
                if self.detect_collision(x, y + d):
                    break
                y += d
                total_moved_abs += abs(d)
        else:
            total_moved_abs = 0
            sign = 1 if dy > 0 else -1
            while total_moved_abs < abs_dy:
                d = min(1, abs_dy - total_moved_abs) * sign
                if self.detect_collision(x, y + d):
                    break
                y += d
                total_moved_abs += abs(d)

            total_moved_abs = 0
            sign = 1 if dx > 0 else -1
            while total_moved_abs < abs_dx:
                d = min(1, abs_dx - total_moved_abs) * sign
                if self.detect_collision(x + d, y):
                    break
                x += d
                total_moved_abs += abs(d)

        return x, y, dx, dy

    def update(self):
        self.move()
        self.sprite.update()

    def draw(self):
        cam = self.world.map.cam
        self.sprite.draw(cam)

        if app.g_debug:
            p.rectb(
                p.floor(self.sprite.position[0] 
                    + self.hitbox.left 
                    - cam.rect.left),
                p.floor(self.sprite.position[1] 
                    + self.hitbox.top 
                    - cam.rect.top
                    + c.HUD_H),
                self.hitbox.w,
                self.hitbox.h,
                8
            )
