import pygame

class InputManager:

    def __init__(self):
        self.map = {'move_left': pygame.K_a,
                    'move_right': pygame.K_d,
                    'jump': pygame.K_w,
                    'attack': pygame.K_r}

    def is_action_pressed(self, action_name: str) -> bool:
        key = pygame.key.get_pressed()

        if key[self.map[action_name]]:
             return True

        return False