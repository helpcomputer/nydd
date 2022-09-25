
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
        pass

    def update(self):
        if self.player.sprite.anim_finished:
            if self.player.vel_x != 0:
                self.state_machine.change("run")
            else:
                self.state_machine.change("idle")

    def draw(self):
        pass
    