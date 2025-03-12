import enum
from dataclasses import dataclass

import pygame
from animation import Animation







class PlayerState(enum.Enum):
    IDLE = 1
    MOVING = 2
    ATTACKING = 3
    JUMPING = 4




class Fighter:

    # constructor
    def __init__(self, x, animations, input_map, xy_offset):

        # ss = pygame.image.load('../assets/images/wizard/Sprites/wizard.png')
        self.ground_y = 500
        self.input_map = input_map
        self.attack_damage = .6
        self.idle_animation = animations['idle']
        self.walk_animation = animations['walk']
        self.attack_animation = animations['attack']
        self.jump_animation = animations['jump']
        self.death_animation = animations['death']

        self.current_animation = self.idle_animation
        self.state = PlayerState.IDLE
        self.rect = pygame.Rect(x, 0, 80, 180)
        self.rect.bottom = self.ground_y
        self.health = 100
        self.vel = 0
        self.facing_right = True
        self.x_offset = xy_offset[0]
        self.y_offset = xy_offset[1]


    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.facing_right:
            screen.blit(self.current_animation.get_frame(), (self.rect.x - self.x_offset, self.rect.y - self.y_offset))
        else:
            img = pygame.transform.flip(self.current_animation.get_frame(), True, False).convert_alpha()
            screen.blit(img, (self.rect.x - self.x_offset, self.rect.y - self.y_offset))

    def idle_state(self, dt):
        self.current_animation.update(dt)

        key = pygame.key.get_pressed()

        if key[self.input_map['walk_left']] or key[self.input_map['walk_right']]:
            self.change_state(PlayerState.MOVING)
        elif key[self.input_map['jump']]:
            self.change_state(PlayerState.JUMPING)
        elif key[self.input_map['attack']]:
            self.change_state(PlayerState.ATTACKING)

    def move_state(self, dt):
        self.current_animation.update(dt)

        SPEED = 10
        dx = 0

        key = pygame.key.get_pressed()

        # d key is down
        if key[self.input_map['walk_right']]:
            dx += SPEED
            self.facing_right = True

            if key[self.input_map['jump']]:
                self.change_state(PlayerState.JUMPING)
        # a key is down
        elif key[self.input_map['walk_left']]:
            dx -= SPEED
            self.facing_right = False

            if key[self.input_map['jump']]:
                self.change_state(PlayerState.JUMPING)
        elif key[self.input_map['attack']]:
            self.change_state(PlayerState.ATTACKING)
        # if you're not moving???
        else:
            self.change_state(PlayerState.IDLE)

        # elif key[pygame.K_e]:
        #     self.current_animation = self.attack_animation
        #     self.attack(screen, opponent)

        self.rect.x += dx

    def attack_state(self, dt, screen, opponent):

        self.current_animation.update(dt)

        self.attack(screen, opponent)

        if self.current_animation.is_finished():
            self.change_state(PlayerState.IDLE)


    def jump_state(self, dt):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()


        # left and right movement
        if key[self.input_map['walk_right']]:
            dx += SPEED
            self.facing_right = True
            # a key is down
        elif key[self.input_map['walk_left']]:
            dx -= SPEED
            self.facing_right = False

        self.vel += GRAVITY

        dy += self.vel

        if self.rect.bottom + dy > self.ground_y:
            self.vel = 0
            self.rect.bottom = self.ground_y
            dy = 0
            # dy = self.ground_y - self.rect.bottom
            self.change_state(PlayerState.IDLE)

        self.rect.x += dx
        self.rect.y += dy

    # you must use change_state to change the players state
    def change_state(self, new_state):
        self.state = new_state

        if self.state == PlayerState.MOVING:
            self.current_animation = self.walk_animation
        elif self.state == PlayerState.IDLE:
            self.current_animation = self.idle_animation
        elif self.state == PlayerState.ATTACKING:
            self.current_animation = self.attack_animation
            self.current_animation.reset()
        elif self.state == PlayerState.JUMPING:
            self.current_animation = self.jump_animation
            self.vel = -30

    def update(self, dt, screen, opponent):

        if self.state == PlayerState.IDLE:
            self.idle_state(dt)
        elif self.state == PlayerState.MOVING:
            self.move_state(dt)
        elif self.state == PlayerState.ATTACKING:
            self.attack_state(dt, screen, opponent)
        elif self.state == PlayerState.JUMPING:
            self.jump_state(dt)

    def take_damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.is_dead = True

    def attack(self, screen, opponent):

        if self.facing_right:
            attack_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        else:
            attack_rect = pygame.Rect(self.rect.centerx - 2 * self.rect.width, self.rect.y, 2 * self.rect.width, self.rect.height)
        # pygame.draw.rect(screen, (0, 0, 255), attack_rect)

        if attack_rect.colliderect(opponent.rect):
            opponent.take_damage(self.attack_damage)



    def move(self, screen, opponent):
        pass
