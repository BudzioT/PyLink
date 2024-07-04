import pygame


class Debug:
    """Debug helper"""
    def __init__(self):
        """Initialize debug helper"""
        # Setup pygame
        pygame.init()
        # Prepare the font
        self.font = pygame.font.Font(None, 28)

    def start(self, msg, y=15, x=15):
        """Write certain information at given position"""
        # Get the main surface
        surface = pygame.display.get_surface()
        # Create a text rendered from given message, get its rectangle
        debug_surface = self.font.render(str(msg), True, "White")
        debug_rect = debug_surface.get_rect(topleft=(x, y))
        # Draw the border around the debug message
        pygame.draw.rect(surface, "Black", debug_rect)
        # Draw the message onto the main surface
        surface.blit(debug_surface, debug_rect)
