import pygame

from animation import Animation
from spritesheet import SpriteSheet


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