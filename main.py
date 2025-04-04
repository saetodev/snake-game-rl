import matplotlib.pyplot as plt
import pygame
import time
import torch

from game import Status, SnakeGame
from helper import Timer
from agent import Agent

WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480

def main():
    pygame.init()
    pygame.display.set_caption("SNAKE RL")

    clock   = pygame.time.Clock()
    window  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    running = True

    game   = SnakeGame(20, 15)
    timer  = Timer(0.0625)

    tile_width  = WINDOW_WIDTH / game.width
    tile_height = WINDOW_HEIGHT / game.height

    agent = Agent()
    agent.model.load_state_dict(torch.load("model.pth", weights_only=True))

    while running:
        # begin frame
        # convert from ms to s
        dt = clock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # update
        if game.status == Status.RUNNING:
            timer.tick(dt)

            if timer.done:
                agent.play_and_train(game)
                timer.reset()
        elif game.status == Status.DONE:
            agent.num_games += 1
            agent.train_on_mini_batch()

            print("Game: ", agent.num_games, "Score: ", game.score)

            game.reset()
            timer.reset()

        # render
        window.fill("lightgray")

        food_x = game.food_position.x * tile_width
        food_y = game.food_position.y * tile_height

        pygame.draw.rect(window, "red", (food_x, food_y, tile_width, tile_height))

        for part in game.snake:
            x = part.x * tile_width
            y = part.y * tile_height

            pygame.draw.rect(window, "darkgreen", (x, y, tile_width, tile_height))

        # end frame
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def other_main():
    game  = SnakeGame(20, 15)
    agent = Agent()

    timeout = Timer(10)

    scores      = []
    mean_scores = []

    high_score = 0

    while agent.num_games < 1000:
        while game.status != Status.DONE:
            start_time = time.time()
            agent.play_and_train(game)
            elapsed_time = time.time() - start_time
            timeout.tick(elapsed_time)

            if timeout.done:
                print("Timedout")
                break

        agent.num_games += 1
        agent.train_on_mini_batch()
        #agent.train_on_memory()

        if game.score > high_score:
            high_score = game.score
            agent.model.save()

        print(f"Game: {agent.num_games}, Score: {game.score}")

        scores.append(game.score)
        mean_scores.append(sum(scores) / agent.num_games)

        game.reset()
        timeout.reset()

    plt.plot(list(range(len(scores))), scores)
    plt.plot(list(range(len(mean_scores))), mean_scores)
    plt.show()

if __name__ == "__main__":
    main()
