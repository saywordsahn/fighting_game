import pygame
from fighter import Fighter
from spritesheet import SpriteSheet

pygame.init()

WIDTH = 1000
HEIGHT = 600
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

bg_image = pygame.image.load('./assets/images/background/background.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))



def load_images(self, sprite_sheet, animation_steps):
    # extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
        temp_img_list = []
        for x in range(animation):
            temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
            temp_img_list.append(
                pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
        animation_list.append(temp_img_list)
        self.vel = 0
        self.is_jumping = False
        self.health = 100
        self.attack_damage = 1
        self.is_dead = False


    return animation_list

fighter1 = Fighter(200, 200)
fighter2 = Fighter(700, 300)

clock = pygame.time.Clock()

def draw_health_bar(health, screen, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

while True:

    dt = clock.tick(60) / 1000

    screen.blit(bg_image, (0, 0))
    draw_health_bar(fighter1.health, screen, 20, 20)
    draw_health_bar(fighter2.health, screen, 580, 20)

    fighter1.update(dt)

    fighter1.draw(screen)
    fighter2.draw(screen)

    fighter1.move(dt, screen, fighter2)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()


    pygame.display.update()