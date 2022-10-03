

import state
import enemies.enemy_actor

DEFAULT_WALK_SPEED = 0.4

class Octoman(enemies.enemy_actor.Enemy):
    def __init__(self, world, defin, x, y):
        super().__init__(world, defin, x, y)

        self.state_machine.states["walk"] = \
            Walk(self, self.state_machine, world)

        self.state_machine.change("walk")

    def update(self):
        super().update()
        self.state_machine.update()

    def draw(self):
        super().draw()
        self.state_machine.draw()


class Walk(state.State):
    def __init__(self, enemy_self, state_machine, world) -> None:
        super().__init__()
        self.name = "walk"
        self.state_machine = state_machine
        self.world = world
        self.enemy_self = enemy_self

    def enter(self, enter_params=None):
        self.enemy_self.sprite.set_state("walk")
        self.enemy_self.vel_x = DEFAULT_WALK_SPEED
        if self.enemy_self.sprite.flip_h:
            self.enemy_self.vel_x *= -1

    def exit(self):
        pass

    def handle_input(self, inputs):
        pass

    def turn_around_at_ledge(self):
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

    def update(self):
        self.turn_around_at_ledge()

    def draw(self):
        pass
