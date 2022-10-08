
import state

class Dead(state.State):
    def __init__(self, player, state_machine, world) -> None:
        super().__init__()
        self.name = "dead"
        self.state_machine = state_machine
        self.world = world
        self.player = player

    def enter(self, params):
        self.player.sprite.visible = False
        self.player.sprite.anim_paused = True
        self.player.vel_y_tween = None
        self.world.add_actor(
            "explosion_up_16x32", 
            self.player.sprite.position[0], 
            self.player.sprite.position[1] - 16
        )

    def exit(self):
        pass

    def handle_input(self, inputs):
        pass

    def update(self):
        pass

    def draw(self):
        pass
