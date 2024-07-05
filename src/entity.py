from math import sin

import pygame


class Entity(pygame.sprite.Sprite):
    """Entity of the game"""
    def __init__(self, group):
        super().__init__(group)

        # Entity's direction
        self.direction = pygame.math.Vector2()

        # Current frame
        self.frame = 0
        # Speed of the animation
        self.animation_speed = 0.1

    def _move(self, speed):
        """Move the entity"""
        # Normalize the direction if entity moves, to prevent speed up
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move the entity, check the collisions
        self.hitbox.x += self.direction.x * speed
        self._collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self._collision("vertical")

        # Apply hitbox position
        self.rect.center = self.hitbox.center

    def wave_value(self):
        """Get value of sinus as image full value alpha"""
        # Store current sinus
        value = sin(pygame.time.get_ticks())
        # If it is beyond the X-Axis, return full alpha
        if value >= 0:
            return 255
        # If it is under, return 0 alpha
        else:
            return 0

    def _collision(self, direction):
        """Handle entity's collisions"""
        # Handle horizontal collisions
        if direction == "horizontal":
            # Go through each object sprite, check collisions
            for sprite in self.object_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # Right collisions (if entity moves right, there can't be left collision)
                    if self.direction.x > 0:
                        # Hug the entity to the wall
                        self.hitbox.right = sprite.hitbox.left
                    # Left collisions
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        # Handle vertical collisions
        if direction == "vertical":
            for sprite in self.object_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # Bottom collisions
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    # Top collisions
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

