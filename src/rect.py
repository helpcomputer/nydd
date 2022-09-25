
def overlap(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and \
            x1 + w1 > x2 and \
            y1 < y2 + h2 and \
            y1 + h1 > y2

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def is_overlapping(self, x, y, w, h):
        return self.x < x + w and \
            self.right > x and \
            self.y < y + h and \
            self.bottom > y
        
    def is_overlapping_other(self, other):
        return self.x < other.right and \
            self.right > other.x and \
            self.y < other.bottom and \
            self.bottom > other.y
            
    @property
    def right(self):
        return self.x + self.w

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h
