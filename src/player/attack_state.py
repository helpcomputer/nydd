
import state

class Attack(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "attack"
        self.state_machine = state_machine
        self.world = world
        self.player = player

    def enter(self, enter_params=None):
        self.player.sprite.set_state("attack")

    def exit(self):
        pass

    def handle_input(self, inputs):
        move_x = 0
        if inputs.pressing("left"):
            move_x += -1

        if inputs.pressing("right"):
            move_x += 1

        self.player.vel_x = move_x * self.player.run_speed

    def update(self):
        if self.player.sprite.anim_finished:
            if self.player.is_falling:
                self.state_machine.change("fall")
            else:
                if self.player.vel_x != 0:
                    self.state_machine.change("run")
                else:
                    self.state_machine.change("idle")
            return

    def draw(self):
        pass
    