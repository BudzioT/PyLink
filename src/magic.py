from random import randint
import os

import pygame

from settings import settings


class Magic:
    """Magic class"""
    def __init__(self, animations):
        """Initialize the magic handler"""
        # Get the animations
        self.animations = animations

        # Load the sound effects
        self.sounds = {
            "heal": pygame.mixer.Sound(os.path.join(settings.BASE_PATH, "../audio/heal.wav")),
            "flame": pygame.mixer.Sound(os.path.join(settings.BASE_PATH, "../audio/Fire.wav")),
            "spark": pygame.mixer.Sound(os.path.join(settings.BASE_PATH, "../audio/spark.wav")),
            "energy_ball": pygame.mixer.Sound(os.path.join(settings.BASE_PATH, "../audio/energy_ball.wav")),
            "shield": pygame.mixer.Sound(os.path.join(settings.BASE_PATH, "../audio/shield.wav")),
        }

    def heal(self, player, strength, cost, group):
        """Heal spell, heal the player"""
        # If player has enough energy to use heal spell
        if player.energy >= cost:
            # Heal him based off the strength
            player.health += strength
            # Drain his energy
            player.energy -= cost

            self.sounds["heal"].play()

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

    def spark(self, player, cost, group):
        """Attack the enemy with spark, boost speed for a while"""
        # Cast it if player has enough energy
        if player.energy >= cost and player.energy_balls_count < 3:
            # Decrease player's energy
            player.energy -= cost

            self.sounds["spark"].play()

            # Boost the player's speed by 2
            player.speed_boost = 2

        # Set the direction of the spell based off player's direction
        direction = self._get_direction(player)

        # Shoot four sparks and offset them
        for offset_multiply in range(1, 6):
            # Create curve offset
            curve_offset = randint(-settings.SIZE // 2, settings.SIZE // 2)

            # Shoot horizontally
            if direction.x:
                # Create offset based off current flame number
                offset_x = (direction.x * offset_multiply) * settings.SIZE + randint(1, 20)

                # Calculate position
                pos_x = player.rect.centerx + offset_x + curve_offset
                pos_y = player.rect.centery + curve_offset

                # Create the spark
                self.animations.create_particles("spark", (pos_x, pos_y), group)

            # Shoot vertically
            else:
                # Get the offset and calculate position based off it
                offset_y = (direction.y * offset_multiply) * settings.SIZE + randint(1, 20)
                pos_x = player.rect.centerx + curve_offset
                pos_y = player.rect.centery + offset_y + curve_offset

                # Create the spark
                self.animations.create_particles("spark", (pos_x, pos_y), group)

    def shield(self, player, cost, group):
        """Cast a shield, defending the player"""
        # If player has enough energy, cast it
        if player.energy >= cost:
            # Drain the player's energy
            player.energy -= cost

            self.sounds["shield"].play()

            # Turn on his shield, let him have 3 of them
            player.shield = 3

    def energy_ball(self, player, cost, group):
        """Place an energy ball"""
        # Place it if player has enough energy
        if player.energy >= cost and player.energy_balls_count < 3:
            # Decrease player's energy
            player.energy -= cost

            self.sounds["energy_ball"].play()

            # Create the energy ball
            ball = EnergyBall(player.rect.center, group)

            # Add the energy ball
            player.energy_balls_count += 1

    def flame(self, player, cost, group):
        """Flame spell, attack the enemy with flame"""
        # If player has enough energy to cast a spell
        if player.energy >= cost:
            # Decrease his energy
            player.energy -= cost

            self.sounds["flame"].play()

            direction = self._get_direction(player)

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

    def _get_direction(self, player):
        """Get direction of the spell based off the player"""
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
        return direction


class EnergyBall(pygame.sprite.Sprite):
    """Energy ball magic spell"""
    def __init__(self, pos, group):
        """Initialize the energy ball"""
        super().__init__(group)
        # Set its position
        self.pos = pos
        # Set the group
        self.group = group
        # Name
        self.sprite_type = "energy_ball"

        # Load energy ball's image and get its rect
        self.image = (pygame.image.load(os.path.join(settings.BASE_PATH,
                                                     "../graphics/particles/energy_ball/energy_ball.png"))
                      .convert_alpha())
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 3,
                                            self.image.get_height() * 3))
        self.rect = self.image.get_rect(topleft=pos)

    #def draw(self):
    #    """Draw the energy ball"""
    #    pygame.display.get_surface().blit(self.image, self.rect)
