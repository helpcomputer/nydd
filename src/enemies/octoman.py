

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

    def update(self):
        pass

    def draw(self):
        pass
