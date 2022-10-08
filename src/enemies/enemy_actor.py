
import pyxel

import constants
import actor
import state_machine
import enemies.got_hit_state
import actor_progress_bar

SHOW_HP_BAR_FRAMES = constants.FPS * 3

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

        self.hp_bar = actor_progress_bar.ActorProgressBar({
            "parent" : self,
            "world" : self.world,
            "max_size": (self.sprite.size[0], 2),
            "max_value" : self.stats.get("hp_max"),
            "update_func" : self._update_hp_bar
        })
        self._update_hp_bar(self.hp_bar)
        self.children.append(self.hp_bar)

        def on_dead_removal_func():
            self.world.add_actor(
                "explosion16", 
                self.sprite.position[0], 
                self.sprite.position[1]
            )
        self.on_dead_removal_func = on_dead_removal_func

    def _update_hp_bar(self, hp_bar):
        hp_bar.value = self.stats.get("hp_now")
        percent = self.stats.get("hp_now")/self.stats.get("hp_max")
        if percent < 0.33:
            hp_bar.bar_col = pyxel.COLOR_RED
        elif percent < 0.66:
            hp_bar.bar_col = pyxel.COLOR_ORANGE
        else:
            hp_bar.bar_col = pyxel.COLOR_GREEN

    def take_damage(self, amount):
        self.stats.set(
            "hp_now", 
            max(0, self.stats.get("hp_now") - amount)
        )

    def on_got_hit(self, params):
        if self.state_machine.current.name != "got_hit":
            # TODO: check for damage amount here.
            self.take_damage(20)
            if self.stats.get("hp_now") == 0:
                self.is_alive = False
                return

            self.hp_bar.visible_time = SHOW_HP_BAR_FRAMES

            change_params = { 
                "return_state" : self.state_machine.current.name
            }
            if (params["attacker_cen_x"] < 
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
