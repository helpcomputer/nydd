
import actor

class Explosion(actor.Actor):
    def __init__(self, world, defin, x, y):
        super().__init__(world, defin, x, y)

        self.apply_gravity_func = actor.empty_callback

    def update(self):
        super().update()

        self.is_alive = not self.sprite.anim_finished

    def draw(self):
        super().draw()
