import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 600

bg_image = pygame.image.load('./assets/images/background/background.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))


while True:

    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()


    pygame.display.update()