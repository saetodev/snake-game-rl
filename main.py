import pygame

from game import SnakeGame, Action, MAP_WIDTH, MAP_HEIGHT

WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 720

TILE_WIDTH  = WINDOW_WIDTH / MAP_WIDTH
TILE_HEIGHT = WINDOW_HEIGHT / MAP_HEIGHT

pygame.init()

clock   = pygame.time.Clock()
window  = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True

snake_game   = SnakeGame()
snake_action = Action.FORWARD

update_time     = 0
update_max_time = 0.0625

done = False

while running:
    dt = clock.get_time() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = event.dict["key"]

            # debug shortcuts
            if key == pygame.K_r:
                snake_game   = SnakeGame()
                snake_action = Action.FORWARD
                update_time  = 0
                done         = False
                break

            if key == pygame.K_a:
                snake_action = Action.LEFT
            elif key == pygame.K_d:
                snake_action = Action.RIGHT

    # update game
    if not done:
        update_time += dt

        if update_time >= update_max_time:
            done = snake_game.step(snake_action)

            snake_action = Action.FORWARD 
            update_time  = 0

    # render game
    window.fill((100, 100, 100))

    fx = snake_game.food[0] * TILE_WIDTH
    fy = snake_game.food[1] * TILE_HEIGHT

    pygame.draw.rect(window, (255, 0, 0), (fx, fy, TILE_WIDTH, TILE_HEIGHT))

    for part in snake_game.snake:
        x = part[0] * TILE_WIDTH
        y = part[1] * TILE_HEIGHT

        pygame.draw.rect(window, (0, 255, 0), (x, y, TILE_WIDTH, TILE_HEIGHT))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()