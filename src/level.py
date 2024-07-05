from random import choice
from random import randint

import pygame

from settings import settings
from tile import Tile
from player import Player
from camera import YSortCameraGroup
from utilities import utilities
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import Animation
from magic import Magic
from upgrade import UpgradeMenu


class Level:
    """Level for the game"""
    def __init__(self):
        """Initialize the level"""
        # Get game's display
        self.surface = pygame.display.get_surface()

        # Game pause flag
        self.pause = False

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

        # Animations
        self.animations = Animation()

        # Magic
        self.magic = Magic(self.animations)

        # User's interface
        self.ui = UI()

        # Create the map
        self._create_map()

        # Upgrade menu
        self.upgrade = UpgradeMenu(self.player)

    def run(self):
        """Run the level"""
        # Draw the level
        self._draw()
        # Display player's statistics
        self.ui.display(self.player)

        # If the game is paused, draw the upgrade menu
        if self.pause:
            self.upgrade.display()

        # Otherwise update all game mechanics
        else:
            # Update positions
            self._update()

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

    def open_menu(self):
        """Open the game's upgrade menu"""
        self.pause = not self.pause

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
                      self.object_sprites, self._damage_player, self._death_particles, self._increase_exp)

    def _create_weapon(self):
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
        # Use the healing spell
        if style == "heal":
            self.magic.heal(self.player, strength, cost, [self.visible_sprites])
        # Use the flame spell
        elif style == "flame":
            self.magic.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])
        # Use the shield spell
        elif style == "shield":
            self.magic.shield(self.player, cost, [self.visible_sprites])
        # Use the energy ball
        elif style == "energy_ball":
            self.magic.energy_ball(self.player, cost, [self.visible_sprites, self.attack_sprites])
        # Use the spark
        elif style == "spark":
            self.magic.spark(self.player, cost, [self.visible_sprites])

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
                        # If it's a grass, destroy it
                        if target.sprite_type == "grass":
                            # Get position for the particles
                            pos = target.rect.center
                            # Create a tiny offset
                            offset = pygame.math.Vector2(0, 40)

                            # Create from three up to seven leafs
                            for leaf in range(randint(3, 6)):
                                # Play the grass particles animation
                                self.animations.grass_particles(pos - offset, [self.visible_sprites])

                            # Destroy the grass
                            target.kill()

                        # If enemy got hit by an energy ball
                        elif target.sprite_type == "enemy" and attack_sprite.sprite_type == "energy_ball":
                            # Create particles
                            self.animations.create_particles("energy_ball", attack_sprite.rect.center,
                                                             [self.visible_sprites])
                            # Destroy the energy ball
                            attack_sprite.kill()

                            # Decrease amount of player's balls
                            self.player.energy_balls_count -= 1

                            # Damage the enemy
                            target.get_damage(self.player, attack_sprite.sprite_type)

                        # If it's an enemy, damage him
                        else:
                            target.get_damage(self.player, attack_sprite.sprite_type)

    def _damage_player(self, value, attack_type):
        """Damage the player based off statistics"""
        # If player is vulnerable, handle damage
        if self.player.vulnerable:
            # If player has a shield
            if self.player.shield > 0:
                # Draw the shield particles
                self.animations.create_particles("shield", self.player.rect.center,
                                                 [self.visible_sprites])
                # Decrease the shield amount
                self.player.shield -= 1
            # Otherwise, decrease the health
            else:
                # Decrease player's health
                self.player.health -= value

            # Get the hit time
            self.player.hit_time = pygame.time.get_ticks()
            # Block him from receiving damage constantly
            self.player.vulnerable = False

            # Reset player's speed boost
            self.player.speed_boost = 0

            # Create some particles
            self.animations.create_particles(attack_type, self.player.rect.center,
                                                  [self.visible_sprites])

    def _increase_exp(self, amount):
        """Increase player's experience points"""
        self.player.exp += amount

    def _death_particles(self, pos, particle_type):
        """Trigger particles when entity died"""
        self.animations.create_particles(particle_type, pos, self.visible_sprites)
