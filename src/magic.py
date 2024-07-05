from random import randint

import pygame

from settings import settings


class Magic:
    """Magic class"""
    def __init__(self, animations):
        """Initialize the magic handler"""
        # Get the animations
        self.animations = animations

    def heal(self, player, strength, cost, group):
        """Heal spell, heal the player"""
        # If player has enough energy to use heal spell
        if player.energy >= cost:
            # Heal him based off the strength
            player.health += strength
            # Drain his energy
            player.energy -= cost

            # Animate the aura particles
            self.animations.create_particles("aura", player.rect.center, group)
            # Don't allow the player to heal him over the limit
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            else:
                # Get a small offset
                offset = pygame.math.Vector2(0, -30)
                # If player has healed not beyond the limit, animate the heal particles
                self.animations.create_particles("heal", player.rect.center + offset, group)

    def shield(self, player, cost, group):
        """Cast a shield, defending the player"""
        # If player has enough energy, cast it
        if player.energy >= cost:
            # Drain the player's energy
            player.energy -= cost

            # Turn on his shield, let him have 3 of them
            player.shield = 3

    def energy_ball(self, player, cost, group):
        """Place an energy ball"""
        # Place it if player has enough energy
        if player.energy >= cost:
            # Decrease player's energy
            player.energy -= cost

    def flame(self, player, cost, group):
        """Flame spell, attack the enemy with flame"""
        # If player has enough energy to cast a spell
        if player.energy >= cost:
            # Decrease his energy
            player.energy -= cost

            # If player is facing right, set the direction of the spell to the right
            if player.state.split('_')[0] == "right":
                direction = pygame.math.Vector2(1, 0)
            # Set direction to the left
            elif player.state.split('_')[0] == "left":
                direction = pygame.math.Vector2(-1, 0)
            # Set direction to up
            elif player.state.split('_')[0] == "up":
                direction = pygame.math.Vector2(0, -1)
            # Otherwise set it to down
            else:
                direction = pygame.math.Vector2(0, 1)

            # Shoot five flames, offset them
            for offset_multiply in range(1, 6):
                # Create curve offset to make the spell not so straight
                curve_offset = randint(-settings.SIZE // 3, settings.SIZE // 3)

                # Shoot horizontally
                if direction.x:
                    # Create offset based off current flame number
                    offset_x = (direction.x * offset_multiply) * settings.SIZE

                    # Calculate position
                    pos_x = player.rect.centerx + offset_x + curve_offset
                    pos_y = player.rect.centery + curve_offset

                    # Create the flame horizontally
                    self.animations.create_particles("flame", (pos_x, pos_y), group)

                # Shoot vertically
                else:
                    # Get the offset and calculate position based off it
                    offset_y = (direction.y * offset_multiply) * settings.SIZE
                    pos_x = player.rect.centerx + curve_offset
                    pos_y = player.rect.centery + offset_y + curve_offset
                    # Create flame vertically
                    self.animations.create_particles("flame", (pos_x, pos_y), group)
