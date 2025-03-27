import random

from enum import Enum

class Action(Enum):
    FORWARD = 0
    LEFT    = 1
    RIGHT   = 2

MAP_WIDTH  = 40
MAP_HEIGHT = 25

def position_in_map(position: tuple[int, int]) -> bool:
    return position[0] >= 0 and position[0] < MAP_WIDTH and position[1] >= 0 and position[1] < MAP_HEIGHT

class SnakeGame: 
    def __init__(self):
        self.snake           = [ (20, 12), (19, 12), (18, 12) ]
        self.snake_direction = (1, 0)

        self.food = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))

        self.score = 0

    def update_snake_direction(self, action: Action):
        if action == Action.LEFT:
            self.snake_direction = (self.snake_direction[1], -self.snake_direction[0])
        elif action == Action.RIGHT:
            self.snake_direction = (-self.snake_direction[1], self.snake_direction[0])

    def position_on_snake(self, position: tuple[int, int]) -> bool:
        for part in self.snake:
            if part[0] == position[0] and part[1] == position[1]:
                return True
            
        return False

    def step(self, action: Action) -> bool:
        self.update_snake_direction(action)

        current_head = self.snake[0]
        next_head    = (current_head[0] + self.snake_direction[0], current_head[1] + self.snake_direction[1])

        if not position_in_map(next_head) or self.position_on_snake(next_head):
            return True

        if next_head[0] == self.food[0] and next_head[1] == self.food[1]:
            self.score += 1
            self.food = (random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1))
        else:
            self.snake.pop()

        self.snake.insert(0, next_head)

        return False