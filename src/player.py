import os

import pygame
from settings import settings


class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self, pos, group, object_sprites):
        super().__init__(group)

        # Load player's image and get its rect
        self.image = pygame.image.load(os.path.join(settings.BASE_PATH,
                                                    "../graphics/test/player.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Hitbox of the player
        self.hitbox = self.rect.inflate(0, -26)

        # Get object sprites
        self.object_sprites = object_sprites

        # Player's direction
        self.direction = pygame.math.Vector2()
        # Speed
        self.speed = 5

    def update(self):
        """Update player's position"""
        self.handle_input()
        self.move(self.speed)

    def handle_input(self):
        """Set player's action based off input"""
        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def move(self, speed):
        """Move the player"""
        # Normalize the direction if player moves, to prevent speed up
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move the player, check the collisions
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")

        # Apply hitbox position
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Handle player's collisions"""
        # Handle horizontal collisions
        if direction == "horizontal":
            # Go through each object sprite, check collisions
            for sprite in self.object_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # Right collisions (if player moves right, there can't be left collision)
                    if self.direction.x > 0:
                        # Hug the player to the wall
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
