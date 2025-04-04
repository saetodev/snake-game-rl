class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

class Timer:
    def __init__(self, max_time: float):
        self.time = 0
        self.max_time = max_time
        self.done = False

    def tick(self, dt: float):
        if self.done:
            return

        self.time += dt

        if self.time >= self.max_time:
            self.done = True

    def reset(self):
        self.time = 0
        self.done = False
