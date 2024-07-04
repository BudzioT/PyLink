import pygame

from settings import settings
from tile import Tile
from player import Player
from camera import YSortCameraGroup
from utilities import utilities


class Level:
    """Level for the game"""
    def __init__(self):
        """Initialize the level"""
        # Get game's display
        self.surface = pygame.display.get_surface()

        # Sprites that are visible
        self.visible_sprites = YSortCameraGroup()
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
        self.visible_sprites.special_draw(self.player)

    def _update(self):
        # Update positions of the level objects
        self.visible_sprites.update()

    def _create_map(self):
        """Create the map"""
        # Map layouts stored in CSV
        layouts = {
            "limit": utilities.import_csv_layout("../map/map_FloorBlocks.csv")
        }

        # Go through every layout
        for style, layout in layouts.items():
            # Go through each row of the map
            for row_index, row in enumerate(settings.MAP):
                pass

        self.player = Player((2000, 1340), [self.visible_sprites],self.object_sprites)
