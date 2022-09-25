
class StateStack:
    def __init__(self):
        self.states = []
        
    def push(self, state):
        self.states.append(state)
        state.enter()
        
    def pop(self):
        top = self.top()
        if top:
            self.states.remove(top)
            top.exit()
        return top
        
    def top(self):
        if self.states:
            return self.states[-1]
        else:
            return None
        
    def update(self, inputs):
        """We only want the top state to be updated,
        UNLESS it returns True, then the state below
        it will also be updated.
        
        Note that only the top state will be reacting
        to input regardless of the return value."""
        top = self.top()
        if top:
            top.handle_input(inputs)
    
        for s in reversed(self.states):
            carry_on = s.update()
            if carry_on == False:
                break
        
    def draw(self):
        """We allow all states in the stack to be drawn,
        one atop another."""
        for s in self.states:
            s.draw()
