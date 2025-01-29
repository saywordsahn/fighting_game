import pygame


class Fighter:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel = 0
        self.is_jumping = False
        self.health = 100
        self.attack_damage = 1
        self.is_dead = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

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

        if key[pygame.K_d]:
            dx += SPEED

        if key[pygame.K_a]:
            dx -= SPEED

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
