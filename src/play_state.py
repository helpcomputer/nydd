
import state
import hud
import world
import main_menu_state
import state_machine
import play_move_state
import play_transition_state
import play_paused_state

class PlayState(state.State):
    def __init__(self, params) -> None:
        super().__init__()

        self.stack = params["stack"]
        self.world = world.World()
        self.hud = hud.Hud(self.world)

        self.state_machine = state_machine.StateMachine()

        params = {
            "play_state" : self,
            "world" : self.world,
            "hud" : self.hud,
        }

        self.state_machine.states["play_move"] = \
            play_move_state.PlayMoveState(
                self.state_machine, params,
            )
        self.state_machine.states["play_transition"] = \
            play_transition_state.PlayTransitionState(
                self.state_machine, params,
            )
        self.state_machine.states["play_paused"] = \
                play_paused_state.PlayPausedState(
                    self.state_machine, params
            )

        self.state_machine.change("play_move")

    def enter(self, enter_params=None):
        pass

    def exit(self):
        self.stack.push(main_menu_state.MainMenuState({
            "stack" : self.stack,
        }))

    def handle_input(self, inputs):
        self.state_machine.handle_input(inputs)

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.world.draw()
        self.hud.draw()
        self.state_machine.draw()
    