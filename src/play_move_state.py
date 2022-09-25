
import state

class PlayMoveState(state.State):
    def __init__(self, state_machine, params) -> None:
        super().__init__()

        self.state_machine = state_machine
        self.play_state = params["play_state"]
        self.world = params["world"]
        self.hud = params["hud"]

    def enter(self, enter_params=None):
        pass

    def exit(self):
        pass

    def handle_input(self, inputs):
        if inputs.tapped("button_start"):
            self.state_machine.change("play_paused", "play_move")
            return

        self.world.player.handle_input(inputs)

    def update(self):
        self.world.update()
        self.hud.update()

        player = self.world.player
        hbox = player.hitbox
        cam = self.world.map.cam
        move_dir = None
        if player.sprite.position[0] + hbox.right > cam.rect.right:
            move_dir = "right"
        elif player.sprite.position[0] + hbox.left < cam.rect.left:
            move_dir = "left"
        elif player.sprite.position[1] + hbox.top < cam.rect.top:
            move_dir = "up"
        elif player.sprite.position[1] + hbox.bottom > cam.rect.bottom:
            move_dir = "down"

        if move_dir is not None:
            self.state_machine.change("play_transition", move_dir)

    def draw(self):
        pass
