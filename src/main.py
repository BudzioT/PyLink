import pygame, sys

from settings import settings
from level import Level


class Game:
    """The entire game mechanics"""
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        # Set up main surface
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("PyZelda")

        # Level of the game
        self.level = Level()

        # Create timer for calculating FPS
        self.timer = pygame.time.Clock()

    def run(self):
        """Run the game"""
        while True:
            # Handle events
            self._get_events()
            # Draw everything
            self._update_surface()
            # Update objects
            self._update_objects()
            # Remain set amount of FPS
            self.timer.tick(settings.FPS)

    def _get_events(self):
        """Get and handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        """Handle keydown events"""
        # Open upgrade menu on 'M' clicked
        if event.key == pygame.K_m:
            self.level.open_menu()


    def _update_surface(self):
        """Update the main surface, draw objects"""
        # Clean the screen
        self.screen.fill("black")
        # Draw the level and update it
        self.level.run()
        # Update the main surface
        pygame.display.update()

    def _update_objects(self):
        """Update all the objects"""


# If file is main, run the game
if __name__ == "__main__":
    game = Game()
    game.run()