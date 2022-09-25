
import state
import tween
import constants

SLIDE_DURATION = 0.5

class PlayTransitionState(state.State):
    def __init__(self, state_machine, params) -> None:
        super().__init__()

        self.state_machine = state_machine
        self.play_state = params["play_state"]
        self.world = params["world"]
        self.hud = params["hud"]

        self.tween_event = None

    def enter(self, dir=None):
        if self.tween_event or dir is None:
            return

        cam = self.world.map.cam
        player = self.world.player

        map_x = cam.rect.x
        map_y = cam.rect.y
        player_x = player.sprite.position[0]
        player_y = player.sprite.position[1]
        pl_hitbox = player.hitbox
        if dir == "right":
            map_x = cam.rect.x + cam.rect.w
            player_x = player.sprite.position[0] + pl_hitbox.w + 2
        elif dir == "left":
            map_x = cam.rect.x - cam.rect.w
            player_x = player.sprite.position[0] - pl_hitbox.w - 2
        elif dir == "up":
            map_y = cam.rect.y - constants.SCREEN_H + constants.HUD_H
            player_y = player.sprite.position[1] - pl_hitbox.h - 2
        elif dir == "down":
            map_y = cam.rect.y + constants.SCREEN_H - constants.HUD_H
            player_y = player.sprite.position[1] + pl_hitbox.h + 2

        map_dist_x = map_x - cam.rect.x
        map_dist_y = map_y - cam.rect.y
        map_start_x = cam.rect.x
        map_start_y = cam.rect.y

        player_dist_x = player_x - player.sprite.position[0]
        player_dist_y = player_y - player.sprite.position[1]
        player_start_x = player.sprite.position[0]
        player_start_y = player.sprite.position[1]

        def apply(value):
            map_dx = map_start_x + (map_dist_x * value)
            map_dy = map_start_y + (map_dist_y * value)
            cam.rect.x = map_dx
            cam.rect.y = map_dy

            player_dx = player_start_x + (player_dist_x * value)
            player_dy = player_start_y + (player_dist_y * value)
            player.sprite.position[0] = player_dx
            player.sprite.position[1] = player_dy

        self.tween_event = tween.TweenEvent(
            tween.Tween(0, 1, SLIDE_DURATION),
            apply
        )

    def exit(self):
        pass

    def handle_input(self, inputs):
        if inputs.tapped("button_start"):
            self.state_machine.change("play_paused", "play_transition")
            return

    def update(self):
        if self.tween_event:
            self.tween_event.update()
            if self.tween_event.is_finished():
                self.tween_event = None
                self.state_machine.change("play_move")

    def draw(self):
        pass