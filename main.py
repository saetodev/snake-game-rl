import pygame

pygame.init()

window  = pygame.display.set_mode((1280, 720))
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((100, 100, 100))

    pygame.display.flip()

pygame.quit()