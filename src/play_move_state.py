
import state
import constants

class PlayMoveState(state.State):
    def __init__(self, state_machine, params) -> None:
        super().__init__()

        self.state_machine = state_machine
        self.play_state = params["play_state"]
        self.world = params["world"]
        self.hud = params["hud"]

        self.hit_pause = 0

    def do_hit_pause(self, secs):
        self.hit_pause = secs

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
        if self.world.player.is_dead():
            self.state_machine.change("play_player_dead")
            return

        if self.world.hit_pause > 0:
            self.do_hit_pause(self.world.hit_pause)
            self.world.hit_pause = 0

        if self.hit_pause > 0:
            self.hit_pause = max(0, self.hit_pause - constants.SECS_PER_FRAME)
        else:
            self.world.update()

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

        self.hud.update()

    def draw(self):
        pass
