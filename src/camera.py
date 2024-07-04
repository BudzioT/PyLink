import os

import pygame.sprite

from settings import settings


class YSortCameraGroup(pygame.sprite.Group):
    """Camera with sprites sorted by Y coordinate"""
    def __init__(self):
        """Initialize the Y-sort camera"""
        super().__init__()
        # Get the game's surface and settings
        self.surface = pygame.display.get_surface()

        # Half screen dimensions
        self.half_width = self.surface.get_width() // 2
        self.half_height = self.surface.get_height() // 2
        # Camera offset
        self.offset = pygame.math.Vector2()

        # Create floor surface and get its rectangle
        self.floor_surface = pygame.image.load(os.path.join(settings.BASE_PATH,
                                                            "../graphics/tilemap/ground.png")).convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def special_draw(self, player):
        """Draw the sprites"""
        # Set offset based off player position
        self.offset.x = player.rect.x - self.half_width
        self.offset.y = player.rect.y - self.half_height

        # Draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.surface.blit(self.floor_surface, floor_offset_pos)

        # Go through each of sprites and draw them based of Y position
        for sprite in sorted(self.sprites(), key=lambda sp: sp.rect.centery):
            # Get offset position of the object
            offset_pos = sprite.rect.topleft - self.offset
            # Draw it
            self.surface.blit(sprite.image, offset_pos)
