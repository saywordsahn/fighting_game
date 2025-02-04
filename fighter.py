import enum

import pygame
from enum import Enum

from spritesheet import SpriteSheet


class FighterState(enum.Enum):
    IDLE = 1,
    WALKING = 2,
    JUMPING = 3,
    ATTACKING = 4

class Facing(enum.Enum):
    LEFT = 1,
    RIGHT = 2

class Animation:

    def __init__(self, images, is_looped: bool):
        self.images = images
        self.current_frame_index = 0
        self.animation_time = .1
        self.current_time = 0
        self.last_updated_time = 0
        self.is_looped = is_looped

    def update(self, dt):
        self.current_time += dt

        if self.current_time > self.last_updated_time + self.animation_time:
            self.current_frame_index += 1
            self.last_updated_time = self.current_time

    def get_image(self):
        return self.images[self.current_frame_index % len(self.images)]

    def reset(self):
        self.current_frame_index = 0
        self.last_updated_time = 0

    def is_finished(self):
        if self.current_frame_index > len(self.images) and not self.is_looped:
            return True

        return False

class Animator:

    def __init__(self):
        warrior = pygame.image.load('assets/images/warrior/Sprites/warrior.png').convert_alpha()
        warrior_ss = SpriteSheet(warrior, (162, 162), 7, 10, 4)
        self.animations = {'idle': Animation(warrior_ss.load_strip((0, 0), 10), True),
                           'walk': Animation(warrior_ss.load_strip((1, 0), 8), True),
                           'attack': Animation(warrior_ss.load_strip((3, 0), 7), False),
                           'jump': Animation(warrior_ss.load_strip((2, 0), 1), True)}
        self.current_animation = self.animations['idle']

    def play(self, animation_name):
        self.current_animation = self.animations[animation_name]

        if not self.current_animation.is_looped:
            self.current_animation.reset()

    def is_stopped(self) -> bool:
        return self.current_animation.is_finished()

    def update(self, dt):
        self.current_animation.update(dt)

    def get_frame(self):
        return self.current_animation.get_image()

class Fighter:

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.facing = Facing.RIGHT
        self.is_attacking = False
        self.health = 100
        self.attack_damage = 10
        self.animator = Animator()
        self.offset = [-285, -200]
        self.change_state(FighterState.IDLE)

    def draw(self, surface: pygame.Surface):
        # pygame.draw.rect(surface, (0, 255, 0), self.rect)
        if self.facing == Facing.RIGHT:
            surface.blit(self.animator.get_frame(), (self.rect.x + self.offset[0], self.rect.y + self.offset[1]))
        else:
            img = pygame.transform.flip(self.animator.get_frame(), True, False).convert_alpha()
            surface.blit(img, (self.rect.x + self.offset[0], self.rect.y + self.offset[1]))

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

    def change_state(self, new_state: FighterState) -> None:
        self.state = new_state
        print('changing state to', new_state)

        if self.state == FighterState.JUMPING:
            self.animator.play('jump')
            self.vel_y = -30
        elif self.state == FighterState.WALKING:
            self.animator.play('walk')
            self.rect.bottom = 600 - 110
        elif self.state == FighterState.IDLE:
            self.animator.play('idle')
            self.rect.bottom = 600 - 110
        elif self.state == FighterState.ATTACKING:
            self.animator.play('attack')
            self.rect.bottom = 600 - 110

    def idle_state(self):
        print('idle state')
        key = pygame.key.get_pressed()

        if key[pygame.K_d] or key[pygame.K_a]:
            self.change_state(FighterState.WALKING)
        elif key[pygame.K_w]:
            self.change_state(FighterState.JUMPING)
        elif key[pygame.K_r]:
            self.change_state(FighterState.ATTACKING)

    def attack_state(self):
        print('attack state')
        if self.animator.is_stopped():
            self.change_state(FighterState.IDLE)

    def jump_state(self):
        print('jumping state')

        SPEED = 5
        GRAVITY = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_d]:
            self.facing = Facing.RIGHT
            dx += SPEED

        if key[pygame.K_a]:
            self.facing = Facing.LEFT
            dx -= SPEED

        self.vel_y += GRAVITY
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom + dy > 600 - 110:
            self.vel_y = 0
            self.change_state(FighterState.IDLE)

    def walk_state(self):
        print('walking state')
        SPEED = 5
        dx = 0

        key = pygame.key.get_pressed()

        if key[pygame.K_d]:
            self.facing = Facing.RIGHT
            dx += SPEED
        elif key[pygame.K_a]:
            self.facing = Facing.LEFT
            dx -= SPEED

        if dx != 0:
            self.rect.x += dx
        else:
            self.change_state(FighterState.IDLE)

        if key[pygame.K_w]:
            self.change_state(FighterState.JUMPING)

    def update(self, dt, screen, target):

        self.animator.update(dt)

        if self.state == FighterState.IDLE:
            self.idle_state()
        elif self.state == FighterState.WALKING:
            self.walk_state()
        elif self.state == FighterState.ATTACKING:
            self.attack_state()
        elif self.state == FighterState.JUMPING:
            self.jump_state()

        # SPEED = 5
        # GRAVITY = 2
        # dx = 0
        # dy = 0
        #
        # key = pygame.key.get_pressed()
        #
        # if not self.is_attacking:
        #     if key[pygame.K_d] and self.state != FighterState.JUMPING:
        #         self.facing = Facing.RIGHT
        #         dx += SPEED
        #         self.state = FighterState.WALKING
        #
        #     if key[pygame.K_a] and self.state != FighterState.JUMPING:
        #         self.facing = Facing.LEFT
        #         dx -= SPEED
        #         self.state = FighterState.WALKING
        #
        #     if key[pygame.K_w] and self.state != FighterState.JUMPING:
        #         self.vel_y = -30
        #         self.state = FighterState.JUMPING
        #
        #     if key[pygame.K_r]:
        #         self.attack(screen, target)
        #
        # self.vel_y += GRAVITY
        # dy += self.vel_y
        #
        # if self.rect.bottom + dy > 600 - 110:
        #     self.vel_y = 0
        #     dy = 600 - 110 - self.rect.bottom
        #     self.state = FighterState.IDLE
        #
        # self.rect.x += dx
        # self.rect.y += dy


