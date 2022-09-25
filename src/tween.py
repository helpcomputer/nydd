
import constants

def linear(time_passed, start, distance, duration):
    return distance * time_passed / duration + start

class Tween:
    def __init__(self, start, finish, duration):
        self.func = linear
        self.start = start
        self.finish = finish
        self.distance = finish - start
        self.current = start
        self.duration = duration
        self.finished = False
        self.elapsed = 0

    def update(self):
        if self.elapsed < self.duration:
            self.elapsed += constants.SECS_PER_FRAME
            
            self.current = self.func(
                self.elapsed, 
                self.start, 
                self.distance, 
                self.duration
            )
  
        if self.elapsed >= self.duration:
            self.current = self.start + self.distance
            self.finished = True
            
    def is_finished(self):
        return self.finished
        
    def value(self):
        return self.current
        
class TweenEvent:
    def __init__(self, the_tween, apply_func) -> None:
        self.tween = the_tween
        self.apply_func = apply_func

    def is_finished(self):
        return self.tween.is_finished()

    def update(self):
        self.tween.update()
        self.apply_func(self.tween.value())
