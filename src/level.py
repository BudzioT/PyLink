from random import choice

import pygame

from settings import settings
from tile import Tile
from player import Player
from camera import YSortCameraGroup
from utilities import utilities
from weapon import Weapon
from ui import UI
from enemy import Enemy


class Level:
    """Level for the game"""
    def __init__(self):
        """Initialize the level"""
        # Get game's display
        self.surface = pygame.display.get_surface()

        # Sprites that are visible
        self.visible_sprites = YSortCameraGroup()
        # Sprites that can be collided with
        self.object_sprites = pygame.sprite.Group()

        # Sprites that can attack
        self.attack_sprites = pygame.sprite.Group()
        # Sprites that can receive damage
        self.damageable_sprites = pygame.sprite.Group()

        # Current active weapon
        self.active_weapon = None

        # User's interface
        self.ui = UI()

        # Create the map
        self._create_map()

    def run(self):
        """Run the level"""
        # Draw the level
        self._draw()
        # Update positions
        self._update()
        # Display player's statistics
        self.ui.display(self.player)

    def _draw(self):
        # Draw all level objects
        self.visible_sprites.special_draw(self.player)

    def _update(self):
        # Update positions of the level objects
        self.visible_sprites.update()
        # Update positions of the enemies
        self.visible_sprites.enemy_update(self.player)

        # Check for collisions resulting in damage
        self._player_attack()

    def _create_map(self):
        """Create the map"""
        # Map layouts stored in CSV
        layouts = {
            "limit": utilities.import_csv_layout("../map/map_FloorBlocks.csv"),
            "object": utilities.import_csv_layout("../map/map_Objects.csv"),
            "grass": utilities.import_csv_layout("../map/map_Grass.csv"),
            "entities": utilities.import_csv_layout("../map/map_Entities.csv")
        }
        # Graphics of the map
        graphics = {
            "grass": utilities.import_folder("../graphics/Grass"),
            "objects": utilities.import_folder("../graphics/objects")
        }
        # Create tiles
        self._create_all_tiles(graphics, layouts)

    def _create_all_tiles(self, graphics, layouts):
        """Create all tiles with different types"""
        # Go through every layout
        for style, layout in layouts.items():
            # Go through each row of the map
            for row_index, row in enumerate(layout):
                # Go through each column of the map
                for column_index, column in enumerate(row):
                    # Check if column isn't an empty space
                    if column != '-1':
                        # Calculate positions of the tile and create it there
                        pos_x = column_index * settings.SIZE
                        pos_y = row_index * settings.SIZE
                        self._create_tile(pos_x, pos_y, style, column, graphics)

    def _create_tile(self, pos_x, pos_y, style, column, graphics):
        """Create tile at given position, based off style"""
        # If it's a limit tile, create it and assign it as invisible
        if style == "limit":
            Tile((pos_x, pos_y), [self.object_sprites],
                 "invisible")
        # Create object
        elif style == "object":
            image = graphics["objects"][int(column)]
            Tile((pos_x, pos_y), [self.visible_sprites, self.object_sprites],
                 "object", image)
        # Create grass
        elif style == "grass":
            # Choose a random grass image
            random_image = choice(graphics["grass"])
            Tile((pos_x, pos_y), [self.visible_sprites, self.object_sprites,
                                  self.damageable_sprites], "grass", random_image)
        # Create entities
        elif style == "entities":
            # If it is a player, put him here
            if column == "394":
                # Create the player and his weapon
                self.player = Player((pos_x, pos_y), [self.visible_sprites], self.object_sprites,
                                     self._create_weapon, self._destroy_weapon,
                                     self._create_magic, self._destroy_magic)
            # Otherwise put an enemy there, based off the ID set the name
            else:
                # Bamboo
                if column == "390":
                    name = "bamboo"
                # Spirit
                elif column == "391":
                    name = "spirit"
                # Racoon
                elif column == "392":
                    name = "raccoon"
                # Squid
                else:
                    name = "squid"
                Enemy(name, (pos_x, pos_y), [self.visible_sprites, self.damageable_sprites],
                      self.object_sprites)

    def _create_weapon(self): # FUTURE IDEA - CREATE A BOMB
        """Create the weapon"""
        self.active_weapon = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def _destroy_weapon(self):
        """Destroy the weapon"""
        # If the weapon exists, destroy it
        if self.active_weapon:
            self.active_weapon.kill()
            # Set it back to nothing
        self.active_weapon = None

    def _create_magic(self, style, strength, cost):
        """Create the magic spell"""
        pass

    def _destroy_magic(self):
        """Destroy the magic spell"""
        pass

    def _player_attack(self):
        """Logic of player's attacks"""
        # If there are sprites that can attack
        if self.attack_sprites:
            # Go through each of them
            for attack_sprite in self.attack_sprites:
                # Check for collisions between attack sprite and damageable ones
                collisions = pygame.sprite.spritecollide(attack_sprite, self.damageable_sprites, False)
                # If there is a collision, go through each target
                if collisions:
                    for target in collisions:
                        # If it's a grass, just kill it
                        if target.sprite_type == "grass":
                            target.kill()
                        # If it's an enemy, damage him
                        else:
                            target.get_damage(self.player, attack_sprite.sprite_type)
