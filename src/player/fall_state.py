
import state

class Fall(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "fall"
        self.state_machine = state_machine
        self.world = world
        self.player = player

    def enter(self, enter_params=None):
        self.player.sprite.set_state("fall")

    def exit(self):
        pass

    def handle_input(self, inputs):
        if inputs.tapped("button_attack"):
            self.state_machine.change("attack")
            return
        
        if inputs.pressing("up") or inputs.pressing("down"):
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

    def update(self):
        if self.player.is_falling == False:
            if self.player.vel_x != 0:
                self.state_machine.change("run")
            else:
                self.state_machine.change("idle")

    def draw(self):
        pass
