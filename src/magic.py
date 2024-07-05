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



    def flame(self):
        """Flame spell, attack the enemy with flame"""
        pass
