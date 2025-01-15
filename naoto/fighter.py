import pygame

class Fighter:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def move(self):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_d]:
            dx += SPEED

        if key[pygame.K_a]:
            dx -= SPEED

        if key[pygame.K_w]:
            self.vel = 30



        self.rect.x += dx
        self.rect.y += dy
