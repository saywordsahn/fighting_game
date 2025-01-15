import pygame

class Fighter:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)

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
            self.vel_y = -30

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy > 600 - 110:
            self.vel_y = 0
            dy = 600 - 110 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy


