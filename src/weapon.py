import os

import pygame

from settings import settings


class Weapon(pygame.sprite.Sprite):
    """Weapon wielded by player"""
    def __init__(self, player, group):
        """Initialize the weapon"""
        super().__init__(group)
        # Get player's and weapon's direction
        self.direction = self._get_direction(player)

        # Create weapon image and load it
        image_path = os.path.join(settings.BASE_PATH,
                                  f"../graphics/weapons/{player.weapon}/{self.direction}.png")
        self.image = pygame.image.load(image_path).convert_alpha()

        # Set placement of the weapon
        self._set_placement(player)

    def _get_direction(self, player):
        """Get current weapon direction"""
        # Get the direction from the player's state
        return player.state.split('_')[0]

    def _set_placement(self, player):
        """Place the weapon where it supposed to be"""
        # If direction of the weapon should be right, place it right next to the middle right point of player
        if self.direction == "right":
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
        elif self.direction == "left":
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
        elif self.direction == "down":
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
        elif self.direction == "up":
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
