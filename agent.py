import numpy as np
import random
import torch

from collections import deque
from helper import Vec2
from game import Action, Status, SnakeGame
from model import LinearNetwork, Trainer

MAX_MEMORY = 5000
BATCH_SIZE = 1000
MINI_BATCH_SIZE = 32

def get_state(game: SnakeGame):
    head = game.snake[0]

    l = head + Vec2(game.direction.y, -game.direction.x)
    r = head + Vec2(-game.direction.y, game.direction.x)
    f = head + game.direction

    return np.array([
        # danger forward
        (game.position_out_of_bounds(f) or game.position_on_snake(f)),

        # danger left
        (game.position_out_of_bounds(l) or game.position_on_snake(l)),

        # danger right
        (game.position_out_of_bounds(r) or game.position_on_snake(r)),

        # move direction
        #game.direction.x,
        #game.direction.y,

        game.direction.x < 0,
        game.direction.x > 0,
        game.direction.y < 0,
        game.direction.x > 0,

        # food location
        game.food_position.x < head.x,
        game.food_position.x > head.x,
        game.food_position.y < head.y,
        game.food_position.y > head.y,
    ], dtype=np.float32)

class Agent:
    def __init__(self):
        self.num_games = 0

        self.epsilon = 0
        self.model   = LinearNetwork(11, 256, 3)
        self.trainer = Trainer(self.model, lr=0.01, gamma=0.9)

        self.memory = deque(maxlen=MAX_MEMORY)
        self.mini_batch = []

    def get_action(self, state):
        action       = [0, 0, 0]
        self.epsilon = 500 - self.num_games

        if random.randint(0, 200) < self.epsilon:
            action[random.randint(0, len(action) - 1)] = 1
        else:
            state   = torch.tensor(state, dtype=torch.float)
            predict = self.model(state)
            action[torch.argmax(predict)] = 1

        return action

    def train_on_memory(self):
        if len(self.memory) < BATCH_SIZE:
            sample = self.memory
        else:
            sample = random.sample(self.memory, BATCH_SIZE)

        for old_state, new_state, action, reward, done in sample:
            self.trainer.train(old_state, new_state, action, reward, done)

    def train_on_mini_batch(self):
        for old_state, new_state, action, reward, done in self.mini_batch:
            self.trainer.train(old_state, new_state, action, reward, done)

        self.mini_batch.clear()

    def play_and_train(self, game: SnakeGame):
        old_state = get_state(game)
        action    = self.get_action(old_state)
        reward    = game.update(Action(np.argmax(action)))
        new_state = get_state(game)
        done      = game.status == Status.DONE

        self.mini_batch.append((old_state, new_state, action, reward, done))

        if len(self.mini_batch) == MINI_BATCH_SIZE:
            self.train_on_mini_batch()

        #self.trainer.train(old_state, new_state, action, reward, done)
        #self.memory.append((old_state, new_state, action, reward, done))

