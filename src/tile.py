import os

import pygame
from settings import settings


class Tile(pygame.sprite.Sprite):
    """Tiles that can be placed in a level"""
    def __init__(self, pos, group, sprite_type, surface=pygame.Surface((settings.SIZE, settings.SIZE))):
        """Initialize the tile"""
        super().__init__(group)

        # Set the type of sprite
        self.sprite_type = sprite_type

        # Load tile image and get its rect
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

        # Hitbox of the tile
        self.hitbox = self.rect.inflate(0, -10)
