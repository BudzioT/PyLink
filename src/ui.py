import pygame

from settings import settings


class UI:
    """User's interface"""
    def __init__(self):
        """Initialize the UI"""
        # Grab the main surface
        self.surface = pygame.display.get_surface()

        # Create a new font
        self.font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)

        # Create bars
        self.health_bar_rect = pygame.Rect(10, 10, settings.HEALTH_BAR_WIDTH, settings.BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, settings.ENERGY_BAR_WIDTH, settings.BAR_HEIGHT)

    def display(self, player):
        """Display the player's statistics"""
        # Show the health and energy bars
        self._show_bar(player.health, player.stats["health"], self.health_bar_rect, settings.HEALTH_COLOR)
        self._show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, settings.ENERGY_COLOR)

        # Show player's experience
        self._show_exp(player.exp)

    def _show_bar(self, current_amount, max_amount, bg_rect, color):
        """Show a bar with given information"""
        # Draw the background
        pygame.draw.rect(self.surface, settings.BG_COLOR, bg_rect)

        # Calculate ratio of statistic and get bar's width from it
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        # Copy the background's rectangle and change its width to the current amount's width
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Draw the current amount bar
        pygame.draw.rect(self.surface, color, current_rect)
        # Draw the bars border
        pygame.draw.rect(self.surface, settings.BORDER_COLOR, bg_rect, 3)

    def _show_exp(self, exp):
        """Show player's experience points"""
        # Render the text (exp is converted first to int, in case of it changing into float. Then to string)
        text_surface = self.font.render(str(int(exp)), False, settings.TEXT_COLOR)

        # Calculate position of experience point text
        pos_x = settings.WIDTH - 20
        pos_y = settings.HEIGHT - 20
        # Create the experience text rectangle
        text_rect = text_surface.get_rect(bottomright=(pos_x, pos_y))

        # Draw the experience's background
        pygame.draw.rect(self.surface, settings.BG_COLOR, text_rect.inflate(10, 10))
        # Blit the experience text onto the main surface
        self.surface.blit(text_surface, text_rect)
        # Draw the frame
        pygame.draw.rect(self.surface, settings.BORDER_COLOR, text_rect.inflate(10, 10), 3)

    def weapon_box(self, left, top):
        """Draw a weapon box"""
        # Get rectangle of box
        box_rect = pygame.Rect(left, top, settings.BOX_SIZE, settings.BOX_SIZE)
        
