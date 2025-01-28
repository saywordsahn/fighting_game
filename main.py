import pygame
from fighter import Fighter
from spritesheet import SpriteSheet

pygame.init()

WIDTH = 1000
HEIGHT = 600
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

bg_image = pygame.image.load('./assets/images/background/background.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))




fighter1 = Fighter(200, 300)
fighter2 = Fighter(700, 300)

clock = pygame.time.Clock()

def draw_health_bar(health, screen, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

while True:

    dt = clock.tick(60) / 1000

    screen.blit(bg_image, (0, 0))
    draw_health_bar(fighter1.health, screen, 20, 20)
    draw_health_bar(fighter2.health, screen, 580, 20)

    fighter1.draw(screen)
    fighter2.draw(screen)

    fighter1.move(dt, screen, fighter2)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()


    pygame.display.update()