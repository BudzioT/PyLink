import os

import pygame
from settings import Settings


class Tile(pygame.sprite.Sprite):
    """Tiles that can be placed in a level"""
    def __init__(self, pos, group):
        """Initialize the tile"""
        super().__init__(group)
        # Get the game's settings
        self.settings = Settings()

        # Load tile image and get its rect
        self.image = (
            pygame.image.load(os.path.join(self.settings.BASE_PATH, "")).convert_alpha())
        self.rect = self.image.get_rect(topleft=pos)
