

import pyxel

import constants
import actor
import state_machine
import utils
import app

import player.idle_state
import player.run_state
import player.attack_state
import player.jump_state
import player.fall_state
import player.climb_state
import player.got_hit_state
import player.dead_state

RUN_SPEED = 1.05
INVINCIBILITY_SECS = 2

class Player(actor.Actor):
    def __init__(self, world, defin, x, y):
        super().__init__(world, defin, x, y)

        self.vel_y_tween = None
        self.run_speed = RUN_SPEED
        self.invincibility_secs = 0

        self.state_machine = state_machine.StateMachine()
        self.state_machine.states["idle"] = \
            player.idle_state.Idle(self, self.state_machine, world)
        self.state_machine.states["run"] = \
            player.run_state.Run(self, self.state_machine, world)
        self.state_machine.states["attack"] = \
            player.attack_state.Attack(self, self.state_machine, world)
        self.state_machine.states["jump"] = \
            player.jump_state.Jump(self, self.state_machine, world)
        self.state_machine.states["fall"] = \
            player.fall_state.Fall(self, self.state_machine, world)
        self.state_machine.states["climb"] = \
            player.climb_state.Climb(self, self.state_machine, world)
        self.state_machine.states["got_hit"] = \
            player.got_hit_state.GotHit(self, self.state_machine, world)
        self.state_machine.states["dead"] = \
            player.dead_state.Dead(self, self.state_machine, world)

        self.state_machine.change("idle")

    def take_damage(self, amount):
        self.stats.set(
            "hp_now", 
            max(0, self.stats.get("hp_now") - amount)
        )
        #print(f"Player took hit, HP now {self.stats.get('hp_now')}")

    def take_hit(self, params):
        #attacker = params["actor"]
        #attack_stat = params["attack_stat"]
        attack_box = params["hitbox"]
        selfbox = self.get_hitbox()
        # TODO: check attack against defence for damage amount.
        self.take_damage(100)
        if self.stats.get("hp_now") > 0:
            self.invincibility_secs = INVINCIBILITY_SECS
            got_hit_params = {"hit_from" : "right"}
            if selfbox.mid_x > attack_box.mid_x:
                got_hit_params["hit_from"] = "left"
            self.state_machine.change("got_hit", got_hit_params)
        else:
            self.state_machine.change("dead")
            return

    def is_dead(self):
        return self.state_machine.current.name == "dead"

    def check_for_hit(self, params):
        if (self.invincibility_secs > 0 
            or self.is_dead()):
            return
        attack_box = params["hitbox"]
        selfbox = self.get_hitbox()
        if selfbox.is_overlapping_other(attack_box):
            self.take_hit(params)
            
    def get_touching_climbable(self):
        "Return tile location tuple."
        x = self.sprite.position[0]
        y = self.sprite.position[1]
        x1 = int((x + self.hitbox.left) // 8)
        y1 = int((y + self.hitbox.top) // 8)
        x2 = int((x + self.hitbox.right - 1) // 8)
        y2 = int((y + self.hitbox.bottom - 1) // 8)
        for yi in range(y1, y2 + 1):
            for xi in range(x1, x2 + 1):
                if self.world.map.is_climbable(xi, yi):
                    return (xi, yi)
        return None

    def handle_input(self, inputs):
        self.state_machine.handle_input(inputs)

    def update_invincibility(self):
        if self.invincibility_secs > 0:
            if pyxel.frame_count % 5 == 0:
                self.sprite.visible = not self.sprite.visible

            self.invincibility_secs = (
                max(0, self.invincibility_secs - constants.SECS_PER_FRAME)
            )
            if self.invincibility_secs == 0:
                self.sprite.visible = True

    def update(self):
        if not self.is_dead():
            super().update()
            
            self.update_invincibility()

            if self.vel_y_tween:
                self.vel_y_tween.update()
                if self.vel_y_tween.is_finished():
                    self.vel_y_tween = None

        self.state_machine.update()

    def draw(self):
        super().draw()
        self.state_machine.draw()

        if app.g_debug:
            utils.text_label(
                0,
                16,
                "{}".format(self.state_machine.current.name)
            )

            utils.text_label(
                0,
                constants.HUD_H + pyxel.FONT_HEIGHT,
                "{}".format(self.sprite.position)
            )
