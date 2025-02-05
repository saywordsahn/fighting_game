import pygame
from animation import Animation

def load_ss(num_cols, row):
    fighter_ss = pygame.image.load('../assets/images/warrior/Sprites/warrior.png')

    images = []

    for i in range(num_cols):
        slice = fighter_ss.subsurface(i * 162, row * 162, 162, 162)
        scaled_slice = pygame.transform.scale(slice, (162 * 4, 162 * 4))
        images.append(scaled_slice)

    return images


class Fighter:

    def __init__(self, x, y):

        self.idle_animation = Animation(load_ss(10, 0))
        self.walk_animation = Animation(load_ss(8, 1))
        self.attack_animation = Animation(load_ss(7, 3))
        self.current_animation = self.idle_animation

        self.rect = pygame.Rect(x, y, 80, 180)
        self.health = 100
        self.vel = 0
        self.facing_right = True

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.facing_right:
            screen.blit(self.current_animation.get_frame(), (self.rect.x - 280, self.rect.y - 220))
        else:
            img = pygame.transform.flip(self.current_animation.get_frame(), True, False).convert_alpha()
            screen.blit(img, (self.rect.x - 280, self.rect.y - 220))


    def update(self, dt):
        self.current_animation.update(dt)

    def take_damage(self, amount):
        self.health -= amount

        if self.health <= 0:
            self.is_dead = True

    def attack(self, screen, opponent):
        attack_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        pygame.draw.rect(screen, (0, 0, 255), attack_rect)

        if attack_rect.colliderect(opponent.rect):
            opponent.take_damage(self.attack_damage)


    def move(self, screen, opponent):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        # d key is down
        if key[pygame.K_d]:
            dx += SPEED
            self.current_animation = self.walk_animation
            self.facing_right = True
        # a key is down
        elif key[pygame.K_a]:
            dx -= SPEED
            self.current_animation = self.walk_animation
            self.facing_right = False
        else:
            self.current_animation = self.idle_animation

        # this should make us jump when our char is on the ground
        if key[pygame.K_w]:
            if not self.is_jumping:
                print('jump')
                self.is_jumping = True
                self.vel = -30

        if key[pygame.K_e]:
            print('attack')
            self.attack(screen, opponent)

        self.vel += GRAVITY
        dy += self.vel

        if self.rect.bottom + dy > 600 - 110:
            self.is_jumping = False
            self.vel = 0
            dy = 600 - 110 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy
