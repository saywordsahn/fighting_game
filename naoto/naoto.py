import pygame
from fighter import Fighter

pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load('../assets/images/background/background.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

fighter1 = Fighter(200, 310)
fighter2 = Fighter(400, 310)

def draw_background():
    screen.blit(bg, (0, 0))


clock = pygame.time.Clock()

while True:
    clock.tick(60)

    draw_background()
    fighter1.draw(screen)
    fighter2.draw(screen)

    fighter1.move(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)





    pygame.display.update()


