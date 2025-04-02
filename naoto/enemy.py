import pygame
from animation import Animation

def load_ss(image, num_cols, row, width, height, scale):

    images = []

    for i in range(num_cols):
        slice = image.subsurface(i * width, row * height, width, height)
        scaled_slice = pygame.transform.scale(slice, (width * scale, height * scale))
        images.append(scaled_slice)

    return images

toaster_bot_animations = {
        'idle': Animation(load_ss(pygame.image.load('../assets/images/Toaster Bot/idle.png'), 5, 0, 530 / 5, 22, 4)),
        # 'walk': Animation(load_ss(warrior_ss, 8, 1, 162, 4)),
        # 'attack': Animation(load_ss(warrior_ss, 7, 3, 162, 4)),
        # 'jump': Animation(load_ss(warrior_ss, 1, 2, 162, 4)),
        # 'death': Animation(load_ss(warrior_ss, 7, 6, 162, 4))
    }

class Enemy:

    def __init__(self, x):
        self.idle_animation = toaster_bot_animations['idle']
        self.current_animation = self.idle_animation
        self.facing_right = True
        self.rect = self.idle_animation.get_frame().get_rect()
        self.x_offset = 0
        self.y_offset = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.facing_right:
            screen.blit(self.current_animation.get_frame(), (self.rect.x - self.x_offset, self.rect.y - self.y_offset))
        else:
            img = pygame.transform.flip(self.current_animation.get_frame(), True, False).convert_alpha()
            screen.blit(img, (self.rect.x - self.x_offset, self.rect.y - self.y_offset))