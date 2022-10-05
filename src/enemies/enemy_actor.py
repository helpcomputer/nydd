

import actor
import state_machine
import enemies.got_hit_state

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

        self.update_func = self.default_update
        self.draw_func = self.default_draw

        self.got_hit = self.on_got_hit

        self.state_machine = state_machine.StateMachine()
        self.state_machine.states["got_hit"] = \
            enemies.got_hit_state.GotHit(self, self.state_machine, world)

    def on_got_hit(self, params):
        if self.state_machine.current.name != "got_hit":
            # TODO: check for damage and death here.

            change_params = { 
                "return_state" : self.state_machine.current.name
            }
            hitbox = params["hitbox"]
            if (hitbox.mid_x < 
                self.sprite.position[0] + self.hitbox.mid_x):
                change_params["hit_from"] = "left"
            else:
                change_params["hit_from"] = "right"

            self.state_machine.change("got_hit", change_params)

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

    def default_update(self):
        super().update()
        self.keep_on_screen()
        self.set_flip()
        self.state_machine.update()

    def default_draw(self):
        super().draw()
        self.state_machine.draw()

    def update(self):
        self.update_func()

    def draw(self):
        self.draw_func()
