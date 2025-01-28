import enum

import pygame
from enum import Enum

from spritesheet import SpriteSheet


class Facing(enum.Enum):
    LEFT = 1,
    RIGHT = 2


class Fighter:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.facing = Facing.RIGHT
        self.is_jumping = False
        self.is_attacking = False
        self.health = 100
        self.attack_damage = 10
        idle = pygame.image.load('assets/images/warrior/Sprites/warrior.png').convert_alpha()
        warrior_idle_ss = SpriteSheet(idle, (162, 162), 7, 10, 4)
        self.images = warrior_idle_ss.load_strip((0, 0), 10)
        self.offset = [-285, -200]


    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
        surface.blit(self.images[0], (self.rect.x + self.offset[0], self.rect.y + self.offset[1]))

    def take_damage(self, amount):
        self.health -= amount

    def attack(self, screen: pygame.Surface, target):
        self.is_attacking = True

        attack_rect = None

        if self.facing == Facing.RIGHT:
            attack_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
            pygame.draw.rect(screen, (255, 0, 0), attack_rect)

        else:
            attack_rect = pygame.Rect(self.rect.centerx - 2 * self.rect.width, self.rect.y, 2 * self.rect.width, self.rect.height)
            pygame.draw.rect(screen, (255, 0, 0), attack_rect)

        if attack_rect.colliderect(target.rect):
            target.take_damage(self.attack_damage)


        self.is_attacking = False

    def move(self, dt, screen, target):
        SPEED = 5
        GRAVITY = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if not self.is_attacking:
            if key[pygame.K_d]:
                self.facing = Facing.RIGHT
                dx += SPEED

            if key[pygame.K_a]:
                self.facing = Facing.LEFT
                dx -= SPEED

            if key[pygame.K_w] and not self.is_jumping:
                self.vel_y = -30
                self.is_jumping = True

            if key[pygame.K_r]:
                self.attack(screen, target)

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy > 600 - 110:
            self.vel_y = 0
            dy = 600 - 110 - self.rect.bottom
            self.is_jumping = False


        self.rect.x += dx
        self.rect.y += dy


