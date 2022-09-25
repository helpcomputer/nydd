
class StateMachine():
    def __init__(self, states=None):
        self.states = states or {}
        self.current = None
        
    def change(self, stateName, enter_params=None):
        assert self.states[stateName]
        
        #print ("changing to state : " + stateName)
        
        #for k,v in self.states.items():
        #    print(k, v)

        if self.current:
            self.current.exit()
        self.current = self.states[stateName]
        self.current.enter(enter_params)

    def handle_input(self, inputs):
        self.current.handle_input(inputs)
    
    def update(self):
        self.current.update()
    
    def draw(self):
        self.current.draw()
