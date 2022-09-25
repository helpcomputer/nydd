
import state
import tween

class Jump(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "jump"
        self.state_machine = state_machine
        self.world = world
        self.player = player

    def enter(self, enter_params=None):
        self.player.sprite.set_state("jump")
        
        dist = 3.2
        start = -3.2
        def apply(value):
            dy = start + (dist * value)
            self.player.vel_y = dy
            #print("{}".format(dy))

        self.player.vel_y_tween = tween.TweenEvent(
            tween.Tween(0, 1, 0.3),
            apply
        )

    def exit(self):
        pass

    def handle_input(self, inputs):
        if inputs.tapped("button_attack"):
            self.state_machine.change("attack")
            return
        
        move_x = 0
        if inputs.pressing("left"):
            move_x += -1

        if inputs.pressing("right"):
            move_x += 1

        self.player.vel_x = move_x * self.player.run_speed

    def update(self):
        if self.player.is_falling:
            self.state_machine.change("fall")
            return

    def draw(self):
        pass
