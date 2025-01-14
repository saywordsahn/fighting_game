import pygame

class Fighter:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)