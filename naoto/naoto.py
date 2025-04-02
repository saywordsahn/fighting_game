import pygame
from fighter import Fighter
from animation import Animation
from enemy import Enemy

pygame.init()

WIDTH = 1000
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load('../assets/images/background/background.jpg')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

def load_ss(image, num_cols, row, size, scale):

    images = []

    for i in range(num_cols):
        slice = image.subsurface(i * size, row * size, size, size)
        scaled_slice = pygame.transform.scale(slice, (size * scale, size * scale))
        images.append(scaled_slice)

    return images


toaster_bot_ss = pygame.image.load('../assets/images/Toaster Bot/all.png')
warrior_ss = pygame.image.load('../assets/images/warrior/Sprites/warrior.png')
wizard_ss = pygame.image.load('../assets/images/wizard/Sprites/wizard.png')

enemy = Enemy(200)

warrior_animations = {
            'idle': Animation(load_ss(warrior_ss, 10, 0, 162, 4)),
            'walk': Animation(load_ss(warrior_ss, 8, 1, 162, 4)),
            'attack': Animation(load_ss(warrior_ss, 7, 3, 162, 4)),
            'jump': Animation(load_ss(warrior_ss, 1, 2, 162, 4)),
            'death': Animation(load_ss(warrior_ss, 7, 6, 162, 4))
        }

warrior_input_map = {
    'walk_left': pygame.K_a,
    'walk_right': pygame.K_d,
    'jump': pygame.K_w,
    'attack': pygame.K_e
}

wizard_animations = {
            'idle': Animation(load_ss(wizard_ss, 8, 0, 250, 3)),
            'walk': Animation(load_ss(wizard_ss, 8, 1, 250, 3)),
            'attack': Animation(load_ss(wizard_ss, 8, 3, 250, 3)),
            'jump': Animation(load_ss(wizard_ss, 2, 2, 250, 3)),
            'death': Animation(load_ss(wizard_ss, 7, 6, 250, 3))
}

wizard_input_map = {
            'walk_left': pygame.K_LEFT,
            'walk_right': pygame.K_RIGHT,
            'jump': pygame.K_UP,
            'attack': pygame.K_KP0
        }




fighter1 = Fighter(200, warrior_animations, warrior_input_map, (280, 220))
fighter2 = Fighter(500, wizard_animations, wizard_input_map, (340, 320))

images = []




def load_ss(image, num_cols, row, size):

    images = []

    for i in range(num_cols):
        slice = image.subsurface(i * size, row * size, size, size)
        scaled_slice = pygame.transform.scale(slice, (size * 4, size * 4))
        images.append(scaled_slice)

    return images

def draw_background():
    screen.blit(bg, (0, 0))

def draw_health(x, y, health, screen):
    ratio = health / 100
    pygame.draw.rect(screen, (255, 255, 0), (x, y, 400 * ratio, 30))


clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000

    draw_background()
    draw_health(20, 20, fighter1.health, screen)
    draw_health(580, 20, fighter2.health, screen)

    fighter1.draw(screen)
    fighter2.draw(screen)
    # enemy.draw(screen)

    fighter1.update(dt, screen, fighter2)
    fighter2.update(dt, screen, fighter1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)





    pygame.display.update()


