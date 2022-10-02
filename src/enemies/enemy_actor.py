

import actor
import state_machine

class Enemy(actor.Actor):
    def __init__(self, world, defin, x, y):
        super().__init__(world, defin, x, y)

        self.hit_wall_callback = self.hit_wall_response
        self.hit_floor_callback = self.hit_floor_response
        self.hit_roof_callback = self.hit_roof_response

        cam_rect = self.world.map.cam.rect
        if x < cam_rect.mid_x:
            self.sprite.flip_h = False
        else:
            self.sprite.flip_h = True

        self.state_machine = state_machine.StateMachine()

    def keep_on_screen(self):
        """Keep full sprite on screen, not just checking the hitbox."""

        cam_rect = self.world.map.cam.rect
        x = self.sprite.position[0]
        y = self.sprite.position[1]
        if x < cam_rect.left:
            x = cam_rect.left
            self.hit_wall_response()
        elif x + self.sprite.size[0] > cam_rect.right:
            x = cam_rect.right - self.sprite.size[0]
            self.hit_wall_response()

        if y < cam_rect.top:
            y = cam_rect.top
            self.hit_roof_response()
        elif y + self.sprite.size[1] > cam_rect.bottom:
            y = cam_rect.bottom - self.sprite.size[1]
            self.hit_floor_response()

        self.sprite.position[0], self.sprite.position[1] = x, y

    def hit_floor_response(self):
        self.vel_y = 0

    def hit_roof_response(self):
        self.vel_y = 0

    def hit_wall_response(self):
        self.vel_x *= -1

    def update(self):
        super().update()
        self.keep_on_screen()
        self.set_flip()

    def draw(self):
        super().draw()
