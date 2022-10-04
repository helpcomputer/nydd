
import pyxel

import state
import actor

CLIMB_SPEED = 0.5

class Climb(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "climb"
        self.state_machine = state_machine
        self.world = world
        self.player = player

    def enter(self, enter_params=None):
        self.player.sprite.set_state("climb")
        self.player.gravity = 0
        self.player.max_fall_speed = 0
        self.player.vel_x = 0
        self.player.vel_y = 0
        self.is_falling = False
        self.player.vel_y_tween = None

        self.player.hit_floor_callback = self.climb_hit_floor
        self.player.apply_gravity_func = actor.empty_callback
        self.player.set_flip_func = actor.empty_callback

    def climb_hit_floor(self):
        self.state_machine.change("idle")

    def exit(self):
        self.player.gravity = actor.DEFAULT_GRAVITY
        self.player.max_fall_speed = actor.DEFAULT_MAX_FALL_SPEED
        self.player.hit_floor_callback = actor.empty_callback
        self.player.apply_gravity_func = None
        self.player.set_flip_func = None

    def handle_input(self, inputs):
        if inputs.pressing("button_jump"):
            self.state_machine.change("fall")
            return

        move_x = 0
        if inputs.pressing("left"):
            move_x += -1
        if inputs.pressing("right"):
            move_x += 1
        
        move_y = 0
        if inputs.pressing("up"):
            move_y += -1
        if inputs.pressing("down"):
            move_y += 1

        climb_speed = CLIMB_SPEED
        if move_x != 0 and move_y != 0:
            climb_speed *= 0.707

        if move_x != 0 or move_y != 0:
            if pyxel.frame_count % 10 == 0:
                self.player.sprite.flip_h = not self.player.sprite.flip_h

        self.player.vel_x = move_x * climb_speed
        self.player.vel_y = move_y * climb_speed

    def update(self):
        self.is_falling = False
        tile = self.player.get_touching_climbable()
        if tile is None:
            self.state_machine.change("idle")

    def draw(self):
        pass
