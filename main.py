import pygame
from fighter import Fighter

pygame.init()

WIDTH = 1000
HEIGHT = 600

bg_image = pygame.image.load('./assets/images/background/background.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

fighter1 = Fighter(200, 300)
fighter2 = Fighter(700, 300)

clock = pygame.time.Clock()

while True:

    dt = clock.tick(60) / 1000

    screen.blit(bg_image, (0, 0))

    fighter1.draw(screen)
    fighter2.draw(screen)

    fighter1.move(dt, screen, fighter2)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()


    pygame.display.update()