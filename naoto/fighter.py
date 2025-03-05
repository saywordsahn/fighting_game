import enum

import pygame
from animation import Animation



def load_ss(image, num_cols, row, size):

    images = []

    for i in range(num_cols):
        slice = image.subsurface(i * size, row * size, size, size)
        scaled_slice = pygame.transform.scale(slice, (size * 4, size * 4))
        images.append(scaled_slice)

    return images



class PlayerState(enum.Enum):
    IDLE = 1
    MOVING = 2
    ATTACKING = 3
    JUMPING = 4


ss = pygame.image.load('../assets/images/warrior/Sprites/warrior.png')


class Fighter:

    def __init__(self, x, y):

        # ss = pygame.image.load('../assets/images/wizard/Sprites/wizard.png')

        self.idle_animation = Animation(load_ss(ss, 10, 0, 162))
        self.walk_animation = Animation(load_ss(ss, 8, 1, 162))
        self.attack_animation = Animation(load_ss(ss, 7, 3, 162))
        self.jump_animation = Animation(load_ss(ss, 1, 2, 162))
        self.death_animation = Animation(load_ss(ss, 7, 6, 162))

        self.current_animation = self.idle_animation
        self.state = PlayerState.IDLE
        self.rect = pygame.Rect(x, y, 80, 180)
        self.health = 100
        self.vel = 0
        self.facing_right = True

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.facing_right:
            screen.blit(self.current_animation.get_frame(), (self.rect.x - 280, self.rect.y - 220))
        else:
            img = pygame.transform.flip(self.current_animation.get_frame(), True, False).convert_alpha()
            screen.blit(img, (self.rect.x - 280, self.rect.y - 220))

    def idle_state(self, dt):
        self.current_animation.update(dt)

        key = pygame.key.get_pressed()

        if key[pygame.K_d] or key[pygame.K_a]:
            self.change_state(PlayerState.MOVING)
        elif key[pygame.K_w]:
            self.change_state(PlayerState.JUMPING)
        elif key[pygame.K_e]:
            self.change_state(PlayerState.ATTACKING)

    def move_state(self, dt):
        self.current_animation.update(dt)

        SPEED = 10
        dx = 0

        key = pygame.key.get_pressed()

        # d key is down
        if key[pygame.K_d]:
            dx += SPEED
            self.facing_right = True

            if key[pygame.K_w]:
                self.change_state(PlayerState.JUMPING)
        # a key is down
        elif key[pygame.K_a]:
            dx -= SPEED
            self.facing_right = False

            if key[pygame.K_w]:
                self.change_state(PlayerState.JUMPING)
        elif key[pygame.K_e]:
            self.change_state(PlayerState.ATTACKING)
        # if you're not moving???
        else:
            self.change_state(PlayerState.IDLE)

        # elif key[pygame.K_e]:
        #     self.current_animation = self.attack_animation
        #     self.attack(screen, opponent)

        self.rect.x += dx

    def attack_state(self, dt):

        self.current_animation.update(dt)

        if self.current_animation.is_finished():
            self.change_state(PlayerState.IDLE)

    def jump_state(self, dt):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()


        # left and right movement
        if key[pygame.K_d]:
            dx += SPEED
            self.facing_right = True
            # a key is down
        elif key[pygame.K_a]:
            dx -= SPEED
            self.facing_right = False

        self.vel += GRAVITY

        dy += self.vel

        if self.rect.bottom + dy > 600 - 110:
            self.vel = 0
            dy = 600 - 110 - self.rect.bottom
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
            self.attack_state(dt)
        elif self.state == PlayerState.JUMPING:
            self.jump_state(dt)

    def take_damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.is_dead = True

    def attack(self, screen, opponent):
        attack_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        # pygame.draw.rect(screen, (0, 0, 255), attack_rect)

        if attack_rect.colliderect(opponent.rect):
            opponent.take_damage(self.attack_damage)



    def move(self, screen, opponent):
        pass
