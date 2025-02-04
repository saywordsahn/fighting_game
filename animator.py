import pygame

from animation import Animation
from spritesheet import SpriteSheet


class Animator:

    def __init__(self):
        self.animations = {}
        self.current_animation = None

    def add_animation(self, animation_name: str, animation):
        self.animations[animation_name] = animation

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