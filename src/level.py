import pygame

from settings import Settings
from tile import Tile
from player import Player


class Level:
    """Level for the game"""
    def __init__(self):
        """Initialize the level"""
        # Get game's display
        self.surface = pygame.display.get_surface()
        # Grab game's settings
        self.settings = Settings()

        # Sprites that are visible
        self.visible_sprites = pygame.sprite.Group()
        # Sprites that can be collided with
        self.object_sprites = pygame.sprite.Group()

        # Create the map
        self._create_map()

    def run(self):
        """Run the level"""
        # Draw the level
        self._draw()
        # Update positions
        self._update()

    def _draw(self):
        # Draw all level objects
        self.visible_sprites.draw(self.surface)

    def _update(self):
        # Update positions of the level objects
        self.visible_sprites.update()

    def _create_map(self):
        """Create the map"""
        # Go through each row of the map
        for index_row, row in enumerate(self.settings.MAP):
            # Go through each column of the map
            for index_column, column in enumerate(row):
                # Get its position
                pos_x = index_column * self.settings.SIZE
                pos_y = index_row * self.settings.SIZE
                # If it's an object, create sprite tile with it
                if column == 'x':
                    Tile((pos_x, pos_y), [self.visible_sprites, self.object_sprites])
                # If it's a player, create sprite of him
                elif column == 'p':
                    self.player = Player((pos_x, pos_y), [self.visible_sprites],
                                         self.object_sprites)
