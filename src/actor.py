
import pyxel as p

import constants as c
import rect
import sprite
import app
import stats
import actor_defs

DEFAULT_GRAVITY = 0.5
DEFAULT_MAX_FALL_SPEED = 2.5

def empty_callback():
    pass

class Actor:
    def __init__(self, world, defin, x, y):
        self.type = defin["type"]
        self.world = world
        self.sprite = sprite.Sprite(defin, x, y)
        self.hitbox = rect.Rect(*(defin.get("hitbox", (8,8,8,8))))
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = DEFAULT_GRAVITY
        self.max_fall_speed = DEFAULT_MAX_FALL_SPEED
        self.is_falling = False
        self.uid = 0
        self.is_alive = True
        self.stats = stats.Stats(
            actor_defs.BASE_STATS.get(self.type, {})
        )
        self.children = []

        self.hit_wall_callback = empty_callback
        self.hit_roof_callback = empty_callback
        self.hit_floor_callback = empty_callback

        self.apply_gravity_func = None
        self.set_flip_func = None

        self.got_hit = None
        self.can_get_hit = None

        self.on_dead_removal_func = None

    def get_hitbox(self):
        x = self.sprite.position[0] + self.hitbox.left
        y = self.sprite.position[1] + self.hitbox.top
        return rect.Rect(x, y, self.hitbox.w, self.hitbox.h)

    def check_hit(self, params):
        if (self.got_hit is None 
            or self.can_get_hit is None
            or self.can_get_hit() == False):
            return False
        hitbox = params["hitbox"]
        selfbox = self.get_hitbox()
        if selfbox.is_overlapping_other(hitbox):
            self.got_hit(params)
            return True
        return False

    def get_state(self):
        return self.sprite.state

    def set_state(self, state):
        self.sprite.set_state(state)

    def move(self):
        last_y = self.sprite.position[1]

        self.apply_gravity()

        pos = self.sprite.position
        pos[0], pos[1] = \
            self.push_back(pos[0], pos[1], self.vel_x, self.vel_y)

        self.is_falling = self.sprite.position[1] > last_y

    def apply_gravity(self):
        if self.apply_gravity_func:
            self.apply_gravity_func()
        else:
            self.vel_y = min(
                self.vel_y + self.gravity, 
                self.max_fall_speed
            )

    def detect_collision(self, x, y, dy=0):
        x1 = int((x + self.hitbox.left) // 8)
        y1 = int((y + self.hitbox.top) // 8)
        x2 = int((x + self.hitbox.right - 1) // 8)
        y2 = int((y + self.hitbox.bottom - 1) // 8)
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                if self.world.map.is_solid(xi, yi):
                    return True
        if dy > 0 and p.floor((y + self.hitbox.bottom) % 8) == 1:
            for xi in range(x1, x2 + 1):
                if self.world.map.is_one_way(xi, y2):
                    return True
        return False

    def push_back_x(self, x, y, dx, abs_dx):
        total_moved_abs = 0
        sign = 1 if dx > 0 else -1
        while total_moved_abs < abs_dx:
            d = min(1, abs_dx - total_moved_abs) * sign
            if self.detect_collision(x + d, y):
                self.hit_wall_callback()
                break
            x += d
            total_moved_abs += abs(d)
        return x

    def push_back_y(self, x, y, dy, abs_dy):
        total_moved_abs = 0
        sign = 1 if dy > 0 else -1
        while total_moved_abs < abs_dy:
            d = min(1, abs_dy - total_moved_abs) * sign
            if self.detect_collision(x, y + d, dy):
                if dy > 0:
                    self.hit_floor_callback()
                else:
                    self.hit_roof_callback()
                break
            y += d
            total_moved_abs += abs(d)
        return y

    def push_back(self, x, y, dx, dy):
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        if abs_dx > abs_dy:
            x = self.push_back_x(x, y, dx, abs_dx)
            y = self.push_back_y(x, y, dy, abs_dy)
        else:
            y = self.push_back_y(x, y, dy, abs_dy)
            x = self.push_back_x(x, y, dx, abs_dx)
        return x, y

    def set_flip(self):
        if self.set_flip_func:
            self.set_flip_func()
        else:
            sig = p.sgn(self.vel_x)
            if sig < 0:
                self.sprite.flip_h = True
            elif sig > 0:
                self.sprite.flip_h = False

    def update(self):
        self.move()
        self.sprite.update()
        self.set_flip()

        for child in self.children:
            child.update()

    def draw(self):
        cam = self.world.map.cam
        self.sprite.draw(cam)

        for child in self.children:
            child.draw()

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
