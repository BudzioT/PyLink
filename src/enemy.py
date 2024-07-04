import pygame

from settings import settings
from entity import Entity
from utilities import utilities


class Enemy(Entity):
    """Enemy class"""
    def __init__(self, name, pos, group, object_sprites):
        """Initialize the enemy"""
        super().__init__(group)

        # Entity's type
        self.sprite_type = "enemy"

        # Enemy graphics
        self._import_graphics(name)
        # Current enemy state
        self.state = "idle"

        # Enemy's surface and rectangle
        self.image = self.animations[self.state][self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        # Hitboxes
        self.hitbox = self.rect.inflate(0, -10)

        # Object sprites (Sprites that have collisions)
        self.object_sprites = object_sprites

        # Enemy statistics
        

    def update(self):
        """Update the enemy"""
        self._move(self.speed)

    def _import_graphics(self, name):
        """Import assets of enemy based off name"""
        self.animations = {"idle": [], "move": [], "attack": []}
        path = f"../graphics/monsters/{name}/"

        # Go through each type of animations
        for animation in self.animations.keys():
            # Import the current animation pack to the list in dictionary
            self.animations[animation] = utilities.import_folder(path + animation)
