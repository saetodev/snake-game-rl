import os
import torch

class LinearNetwork(torch.nn.Module):
    def __init__(self, num_inputs: int, num_hidden: int, num_outputs: int):
        super().__init__()

        self.linear_relu_stack = torch.nn.Sequential(
                torch.nn.Linear(num_inputs, num_hidden),
                torch.nn.ReLU(),
                torch.nn.Linear(num_hidden, num_outputs))

    def forward(self, X):
        return self.linear_relu_stack(X)

    def save(self):
        torch.save(self.state_dict(), "model.pth")

class Trainer:
    def __init__(self, model: LinearNetwork, lr: float, gamma: float):
        self.model = model
        self.gamma = gamma
        self.lr = lr

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = torch.nn.MSELoss()

    def train(self, old_state, new_state, action, reward: float, done: bool):
        old_state = torch.tensor(old_state, dtype=torch.float)
        new_state = torch.tensor(new_state, dtype=torch.float)
        action    = torch.tensor(action, dtype=torch.float)

        predicted = self.model(old_state)
        expected  = predicted.clone()

        Q = reward

        if done:
            Q += self.gamma * torch.max(self.model(new_state))

        expected[torch.argmax(action)] = Q

        self.optimizer.zero_grad()
        loss = self.criterion(expected, predicted)
        loss.backward()
        self.optimizer.step()
