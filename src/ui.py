import os

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

        # Get weapon graphics as a list of loaded images
        self.weapon_graphics = []
        self._convert_weapon_dict()

        # Get list of loaded magic's images
        self.magic_graphics = []
        self._convert_magic_dict()

    def display(self, player):
        """Display the player's statistics"""
        # Show the health and energy bars
        self._show_bar(player.health, player.stats["health"], self.health_bar_rect, settings.HEALTH_COLOR)
        self._show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, settings.ENERGY_COLOR)

        # Show player's experience
        self._show_exp(player.exp)

        # Show the melee weapon box
        self._weapon_overlay(player.weapon_index, not player.can_weapon_switch)
        # Show the magic box
        self._magic_overlay(player.magic_index, not player.can_magic_switch)

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

    def _weapon_box(self, left, top, switch):
        """Draw a weapon box"""
        # Get rectangle of box
        box_rect = pygame.Rect(left, top, settings.BOX_SIZE, settings.BOX_SIZE)
        # Draw the background
        pygame.draw.rect(self.surface, settings.BG_COLOR, box_rect)

        # Draw the frame with color based off if the player is currently changing weapon
        # If the player has switched weapon, draw it in active color
        if switch:
            pygame.draw.rect(self.surface, settings.BORDER_ACTIVE_COLOR, box_rect, 3)
        # Otherwise, draw it in the normal color
        else:
            pygame.draw.rect(self.surface, settings.BORDER_COLOR, box_rect, 3)

        # Return the box's rectangle
        return box_rect

    def _weapon_overlay(self, weapon_index, switch):
        """Display proper weapon in the box"""
        # Show the melee weapon box and get its rectangle
        box_rect = self._weapon_box(10, 630, switch)

        # Get the weapon's surface from a list based off current weapon index
        weapon_surface = self.weapon_graphics[weapon_index]
        # Place it at the center of the weapon box
        weapon_rect = weapon_surface.get_rect(center=box_rect.center)

        # Blit the weapon onto the main surface
        self.surface.blit(weapon_surface, weapon_rect)

    def _magic_overlay(self, magic_index, switch):
        """Display the correct magic in magic's box"""
        # Draw the magic's box rectangle and save it
        box_rect = self._weapon_box(80, 635, not switch)

        # Get magic's surface based off current magic index
        magic_surface = self.magic_graphics[magic_index]
        # Center it in a weapon magic box
        magic_rect = magic_surface.get_rect(center=box_rect.center)

        # Blit the spell
        self.surface.blit(magic_surface, magic_rect)

    def _convert_weapon_dict(self):
        """Convert weapons from dictionary to a list"""
        # Go through each weapon
        for weapon in settings.weapon_info.values():
            # Grab its image path and load it
            path = weapon["graphic"]
            weapon = pygame.image.load(os.path.join(settings.BASE_PATH, path)).convert_alpha()
            # Add it to the list
            self.weapon_graphics.append(weapon)

    def _convert_magic_dict(self):
        """Convert magic spells into a list of loaded images"""
        # Iterate through each of magic's spells
        for magic in settings.magic_info.values():
            # Save and load its image
            path = magic["graphic"]
            magic = pygame.image.load(os.path.join(settings.BASE_PATH, path)).convert_alpha()
            # Append it
            self.magic_graphics.append(magic)
