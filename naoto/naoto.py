import pygame
from fighter import Fighter

pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load('../assets/images/background/background.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

fighter1 = Fighter(200, 310)
fighter2 = Fighter(500, 310)

images = []






def draw_background():
    screen.blit(bg, (0, 0))

def draw_health(x, y, health, screen):
    ratio = health / 100
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 400 * ratio, 30))


clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000

    draw_background()
    draw_health(20, 20, fighter1.health, screen)
    draw_health(580, 20, fighter2.health, screen)

    fighter1.update(dt)
    fighter2.update(dt)

    fighter1.draw(screen)
    fighter2.draw(screen)

    fighter1.move(screen, fighter2)
    fighter2.move(screen, fighter1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)





    pygame.display.update()


