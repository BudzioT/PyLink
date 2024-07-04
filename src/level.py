import pygame


class Level:
    """Level for the game"""
    def __init__(self):
        """Initialize the level"""
        # Get game's display
        self.surface = pygame.display.get_surface()

        # Sprites that are visible
        self.visible_sprites = pygame.sprite.Group()
        # Sprites that can be collided with
        self.object_sprites = pygame.sprite.Group()

    def run(self):
        """Run the level"""
        pass
