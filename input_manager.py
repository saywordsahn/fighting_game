import pygame

class InputManager:

    def __init__(self):
        self.map = {}

    def add_binding(self, action_name: str, pygame_key):
        """uses the pygame key bindings (ex. pygame.K_a)"""
        self.map[action_name] = pygame_key

    def is_action_pressed(self, action_name: str) -> bool:
        key = pygame.key.get_pressed()
        key[pygame.K_a]
        if key[self.map[action_name]]:
             return True

        return False