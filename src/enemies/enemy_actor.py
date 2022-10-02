

import actor
import state_machine

class Enemy(actor.Actor):
    def __init__(self, world, defin, x, y):
        super().__init__(world, defin, x, y)

        self.state_machine = state_machine.StateMachine()

    def update(self):
        super().update()
        self.state_machine.update()

    def draw(self):
        super().draw()
        self.state_machine.draw()
