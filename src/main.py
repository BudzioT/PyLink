import sys
import os

import pygame

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

        # Main music
        self.music = pygame.mixer.Sound(os.path.join(settings.BASE_PATH, "../audio/main.ogg"))
        self.music.set_volume(0.4)
        # Play it in loop
        self.music.play(loops=-1)

        # Load the death sound and lower its volume
        self.death_sound = pygame.mixer.Sound(os.path.join(settings.BASE_PATH, "../audio/death.wav"))
        self.death_sound.set_volume(0.2)

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

            # Reset the game if player lost
            if self.level.end:
                self.level = Level()
                self.death_sound.play()

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
        self.screen.fill(settings.WATER_COLOR)
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