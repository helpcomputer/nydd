
import state

class Run(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "run"
        self.state_machine = state_machine
        self.world = world
        self.player = player

    def enter(self, enter_params=None):
        self.player.sprite.set_state("run")

    def exit(self):
        pass

    def handle_input(self, inputs):
        if inputs.tapped("button_attack"):
            self.player.vel_x = 0
            self.state_machine.change("attack")
            return

        if inputs.pressing("button_jump"):
            self.state_machine.change("jump")
            return

        if inputs.pressing("up"):
            tile = self.player.get_touching_climbable()
            if tile is not None:
                self.state_machine.change("climb")
            return
        
        move_x = 0
        if inputs.pressing("left"):
            move_x += -1

        if inputs.pressing("right"):
            move_x += 1

        self.player.vel_x = move_x * self.player.run_speed

        if move_x == 0:
            self.state_machine.change("idle")
            return

    def update(self):
        if self.player.is_falling:
            self.state_machine.change("fall")

    def draw(self):
        pass
