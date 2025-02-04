import pygame

from animator import Animator
from animation import Animation
from fighter import Fighter
from input_manager import InputManager
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

input1 = InputManager()
input1.add_binding('move_left', pygame.K_a)
input1.add_binding('move_right', pygame.K_d)
input1.add_binding('jump', pygame.K_w)
input1.add_binding('attack', pygame.K_r)

input2 = InputManager()
input2.add_binding('move_left', pygame.K_LEFT)
input2.add_binding('move_right', pygame.K_RIGHT)
input2.add_binding('jump', pygame.K_UP)
input2.add_binding('attack', pygame.K_KP0)

f1_animator = Animator()

warrior = pygame.image.load('assets/images/warrior/Sprites/warrior.png').convert_alpha()
warrior_ss = SpriteSheet(warrior, (162, 162), 7, 10, 4)
f1_animator.add_animation('idle', Animation(warrior_ss.load_strip((0, 0), 10), True))
f1_animator.add_animation('walk', Animation(warrior_ss.load_strip((1, 0), 8), True))
f1_animator.add_animation('attack', Animation(warrior_ss.load_strip((3, 0), 7), False))
f1_animator.add_animation('jump', Animation(warrior_ss.load_strip((2, 0), 1), True))


f2_animator = Animator()

wizard = pygame.image.load('assets/images/wizard/Sprites/wizard.png').convert_alpha()
wizard_ss = SpriteSheet(wizard, (250, 250), 7, 8, 3)
f2_animator.add_animation('idle', Animation(wizard_ss.load_strip((0, 0), 8), True))
f2_animator.add_animation('walk', Animation(wizard_ss.load_strip((1, 0), 8), True))
f2_animator.add_animation('attack', Animation(wizard_ss.load_strip((3, 0), 8), False))
f2_animator.add_animation('jump', Animation(wizard_ss.load_strip((2, 0), 2), True))


fighter1 = Fighter(200, 200, input1, f1_animator)
fighter2 = Fighter(700, 300, input2, f2_animator)

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


    fighter1.draw(screen)
    fighter2.draw(screen)

    fighter1.update(dt, screen, fighter2)
    fighter2.update(dt, screen, fighter1)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()


    pygame.display.update()