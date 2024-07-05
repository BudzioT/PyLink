import pygame

from settings import settings


class UpgradeMenu:
    """Upgrade menu class"""
    def __init__(self, player):
        """Initialize the upgrade menu"""
        # Get main surface
        self.surface = pygame.display.get_surface()
        # Get the player
        self.player = player

        # Number of attributes
        self.attribute_number = len(player.stats)
        # Names of attributes
        self.attribute_names = list(player.stats.keys())

        # Font
        self.font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)

        # Current selected attribute index
        self.select_index = 0
        # Timer for selection
        self.select_time = None
        # Flag to be able to select attributes
        self.can_select = True

    def display(self):
        """Display the upgrade menu"""
        # Draw the background
        self.surface.fill("black")

        # Handle input
        self._handle_input()
        # Handle cooldown
        self._select_cooldown()

    def _handle_input(self):
        """Handle the input"""
        # Get the keys pressed
        keys = pygame.key.get_pressed()
        if self.can_select:
            if keys[pygame.K_RIGHT] or keys[pygame.K_a]:
                self.select_index += 1
                self.select_time = pygame.time.get_ticks()
                self.can_select = False

            elif keys[pygame.K_LEFT] or keys[pygame.K_d]:
                self.select_index -= 1
                self.select_time = pygame.time.get_ticks()
                self.can_select = False

            if keys[pygame.K_SPACE]:
                pass

    def _select_cooldown(self):
        """Handle the cooldown of attribute selection"""
        if not self.can_select:
            current_time = pygame.time.get_ticks()
            if current_time - self.select_time >= 400:
                self.can_select = True
