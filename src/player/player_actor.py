

import pyxel as p

import constants as c
import actor
import state_machine
import utils
import app
import stats

import player.idle_state
import player.run_state
import player.attack_state
import player.jump_state
import player.fall_state

RUN_SPEED = 1.05

class Player(actor.Actor):
    def __init__(self, world, defin, x, y):
        super().__init__(world, defin, x, y)

        self.vel_y_tween = None
        self.run_speed = RUN_SPEED
        self.stats = stats.Stats()

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
        #self.state_machine.states["ladder"] = \
        #    Ladder(self, self.state_machine, world)

        self.state_machine.change("idle")

    def handle_input(self, inputs):
        self.state_machine.handle_input(inputs)

    def update(self):
        super().update()
        self.state_machine.update()

        if self.vel_y_tween:
            self.vel_y_tween.update()
            if self.vel_y_tween.is_finished():
                self.vel_y_tween = None

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
                c.HUD_H + p.FONT_HEIGHT,
                "{}".format(self.sprite.position)
            )

        #print(self.state_machine.current.name)


