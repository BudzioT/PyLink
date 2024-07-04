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

        # Load tile image
        self.image = surface

        # If sprite isn't an object, create its rect normally
        if sprite_type != "object":
            self.rect = self.image.get_rect(topleft=pos)
        # Otherwise offset the top position by tile size (objects are 2 times higher than other tiles)
        else:
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - settings.SIZE))

        # Hitbox of the tile
        self.hitbox = self.rect.inflate(0, -10)
