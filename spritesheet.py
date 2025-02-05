import pygame

class SpriteSheet:

    def __init__(self, image, cell_size, num_rows, num_cols, scale=1):
        self.image = image
        self.cell_size = cell_size
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.scale = scale

    def get_image(self, row, col, scale=1):
        """
        Get a single image from a SpriteSheet
        :param row: the row in the SpriteSheet (top = 0)
        :param col: the col in the SpriteSheet (left = 0)
        :param scale: how much scale should be applied to the original SpriteSheet
        :return: The image from the SpriteSheet, scaled
        """
        image = pygame.Surface((self.cell_size[0], self.cell_size[1])).convert_alpha()
        image.blit(self.image, (0, 0), (col * self.cell_size[0], row * self.cell_size[1], self.cell_size[0], self.cell_size[1]))

        image = pygame.transform.scale(image, (self.cell_size[0] * self.scale, self.cell_size[1] * self.scale))
        image.set_colorkey((0, 0, 0))
        return image

    def load_strip(self, start, num_frames):
        strip = []

        row = start[0]
        col = start[1]

        while num_frames > 0:

            if col >= self.num_cols:
                row += 1
                col = 0
            else:
                image = self.get_image(row, col, self.scale)
                strip.append(image)
                col += 1
                num_frames -= 1

        return strip





