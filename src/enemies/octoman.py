
import pyxel

import constants
import state
import enemies.enemy_actor
import rect
import app

DEFAULT_WALK_SPEED = 0.4
DEFAULT_ATTACK_SPEED = 2
TURN_AROUND_FRAME_LIMIT = constants.FPS

class Octoman(enemies.enemy_actor.Enemy):
    def __init__(self, world, defin, x, y):
        super().__init__(world, defin, x, y)

        self.state_machine.states["walk"] = \
            Walk(self, self.state_machine, world)
        self.state_machine.states["attack"] = \
            Attack(self, self.state_machine, world)

        self.state_machine.change("walk")

    def update(self):
        super().update()

    def draw(self):
        super().draw()


class Walk(state.State):
    def __init__(self, enemy_self, state_machine, world) -> None:
        super().__init__()
        self.name = "walk"
        self.state_machine = state_machine
        self.world = world
        self.enemy_self = enemy_self

        self.last_turn_frame = 0

    def enter(self, enter_params=None):
        self.enemy_self.sprite.set_state(self.name)
        self.enemy_self.vel_x = DEFAULT_WALK_SPEED
        if self.enemy_self.sprite.flip_h:
            self.enemy_self.vel_x *= -1

    def exit(self):
        pass

    def handle_input(self, inputs):
        pass

    def turn_around_at_ledge(self):
        """Turns around at any gap found of an 8x tile."""

        # If we are turning around too quickly we might be stuck on a small
        # ledge, so just walk off the ledge.
        if (pyxel.frame_count - self.last_turn_frame < 
            TURN_AROUND_FRAME_LIMIT):
            return

        tile_x = self.enemy_self.sprite.position[0]
        if self.enemy_self.vel_x > 0:
            tile_x += self.enemy_self.hitbox.right + 1
        else:
            tile_x += self.enemy_self.hitbox.left + 1
        tile_x //= 8
        tile_y = (self.enemy_self.sprite.position[1] \
            + self.enemy_self.hitbox.bottom + 1) \
            // 8

        if not self.world.map.is_solid(tile_x, tile_y):
            self.enemy_self.vel_x *= -1
            self.enemy_self.set_flip()
            self.last_turn_frame = pyxel.frame_count

    def check_to_attack(self):
        player = self.world.player
        check_area = rect.Rect(0,0,48,8)
        check_area.x = self.enemy_self.sprite.position[0] + 16
        check_area.y = self.enemy_self.sprite.position[1] + 4
        if self.enemy_self.sprite.flip_h:
            check_area.x -= 16 + check_area.w
        player_box = rect.Rect(
            player.sprite.position[0],
            player.sprite.position[1],
            16,
            16
        )
        if check_area.is_overlapping_other(player_box):
            return True
        return False

    def update(self):
        self.turn_around_at_ledge()

        if pyxel.frame_count % 30 == 0:
            if self.check_to_attack():
                self.state_machine.change("attack")

    def draw(self):
        pass


class Attack(state.State):
    def __init__(self, enemy_self, state_machine, world) -> None:
        super().__init__()
        self.name = "attack"
        self.state_machine = state_machine
        self.world = world
        self.enemy_self = enemy_self

        self.started_attack_move = False

    def enter(self, enter_params=None):
        self.enemy_self.sprite.set_state(self.name)
        self.enemy_self.vel_x = 0
        self.started_attack_move = False

    def exit(self):
        pass

    def handle_input(self, inputs):
        pass

    def get_attack_box(self):
        return rect.Rect(
            (self.enemy_self.sprite.position[0] 
                + (0 if self.enemy_self.sprite.flip_h else 8)),
            self.enemy_self.sprite.position[1] + 4,
            8,
            8
        )

    def update(self):
        if self.enemy_self.sprite.anim_finished:
            self.state_machine.change("walk")
            return

        if self.enemy_self.sprite.frame == 1:
            if self.started_attack_move:
                # Better to check this before attack starts this frame so that
                # the player can see at least one frame of attack before 
                # they're hit.
                params = {
                    "actor" : self.enemy_self,
                    "hitbox" : self.get_attack_box(),
                    "attack" : self.enemy_self.stats.get("attack")
                }
                self.world.player.check_for_hit(params)

            else:
                self.started_attack_move = True
                self.enemy_self.vel_x = DEFAULT_ATTACK_SPEED
                if self.enemy_self.sprite.flip_h:
                    self.enemy_self.vel_x *= -1

    def draw(self):
        if app.g_debug:
            cam = self.world.map.cam
            ab = self.get_attack_box()
            ab.x -= cam.rect.left
            ab.y -= cam.rect.top - constants.HUD_H
            ab.draw(pyxel.COLOR_WHITE)
