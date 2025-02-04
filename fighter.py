import enum

import pygame
from enum import Enum

from animator import Animator
from input_manager import InputManager
from spritesheet import SpriteSheet


class FighterState(enum.Enum):
    IDLE = 1,
    WALKING = 2,
    JUMPING = 3,
    ATTACKING = 4

class Facing(enum.Enum):
    LEFT = 1,
    RIGHT = 2





class Fighter:

    def __init__(self, x, y, input_manager, animator):
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.facing = Facing.RIGHT
        self.is_attacking = False
        self.health = 100
        self.attack_damage = 10
        self.animator = animator
        self.offset = [-285, -200]
        self.change_state(FighterState.IDLE)
        self.input_manager = input_manager

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

        if self.input_manager.is_action_pressed('move_left') or self.input_manager.is_action_pressed('move_right'):
            self.change_state(FighterState.WALKING)
        elif self.input_manager.is_action_pressed('jump'):
            self.change_state(FighterState.JUMPING)
        elif self.input_manager.is_action_pressed('attack'):
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

        if self.input_manager.is_action_pressed('move_right'):
            self.facing = Facing.RIGHT
            dx += SPEED

        if self.input_manager.is_action_pressed('move_left'):
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

        if self.input_manager.is_action_pressed('move_right'):
            self.facing = Facing.RIGHT
            dx += SPEED
        elif self.input_manager.is_action_pressed('move_left'):
            self.facing = Facing.LEFT
            dx -= SPEED

        if dx != 0:
            self.rect.x += dx
        else:
            self.change_state(FighterState.IDLE)

        if self.input_manager.is_action_pressed('jump'):
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