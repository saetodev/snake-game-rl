# TODO: we should clearly define the game
# lose condition: the snake goes out of bounds or eats itself
# win condition: maybe when we reach a certain score we win?
#
# we should only reward the agent when it eats food

import random

from collections import deque
from enum import Enum
from helper import Vec2

GOOD_REWARD = 10
BAD_REWARD  = -10

class Action(Enum):
    FORWARD = 0
    LEFT    = 1
    RIGHT   = 2

class Status(Enum):
    DONE    = 0
    RUNNING = 1
    PAUSED  = 2

class SnakeGame:
    def __init__(self, width: int, height: int):
        self.width  = width
        self.height = height
        self.snake  = deque()

        self.reset()

    def reset(self):
        self.score     = 0
        self.status    = Status.RUNNING
        self.direction = Vec2(1, 0)
        
        self.snake.clear()

        cx = int(self.width / 2)
        cy = int(self.height / 2)

        self.snake.append(Vec2(cx, cy))
        self.snake.append(Vec2(cx - 1, cy))
        self.snake.append(Vec2(cx - 2, cy))

        self.set_food_position()

    def set_direction(self, action: Action):
        if action == Action.LEFT:
            self.direction = Vec2(self.direction.y, -self.direction.x)
        elif action == Action.RIGHT:
            self.direction = Vec2(-self.direction.y, self.direction.x)

    def set_food_position(self):
        pos = Vec2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        while self.position_on_snake(pos):
            pos = Vec2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        self.food_position = pos

    def position_out_of_bounds(self, position: Vec2) -> bool:
        return position.x < 0 or position.x >= self.width or position.y < 0 or position.y >= self.height

    def position_on_snake(self, position: Vec2) -> bool:
        for part in self.snake:
            if part == position:
                return True

        return False

    def update(self, action: Action) -> int:
        if self.status == Status.PAUSED:
            return 0

        self.set_direction(action)

        current_pos = self.snake[0]
        next_pos    = current_pos + self.direction

        if self.position_out_of_bounds(next_pos) or self.position_on_snake(next_pos):
            self.status = Status.DONE
            return BAD_REWARD

        reward = 0

        if next_pos == self.food_position:
            reward = GOOD_REWARD
            self.score += 1
            self.set_food_position()
        else:
            self.snake.pop()

        self.snake.appendleft(next_pos)

        return reward
