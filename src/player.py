import os

import pygame

from settings import settings
from utilities import utilities


class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self, pos, group, object_sprites, create_weapon, destroy_weapon):
        super().__init__(group)

        # Load player's image and get its rect
        self.image = pygame.image.load(os.path.join(settings.BASE_PATH,
                                                    "../graphics/test/player.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Import player's assets
        self._import_assets()
        # Set player's state
        self.state = "down"
        # Current frame
        self.frame = 0
        # Speed of the animation
        self.animation_speed = 0.1

        # Hitbox of the player
        self.hitbox = self.rect.inflate(0, -26)

        # Get object sprites
        self.object_sprites = object_sprites

        # Player's direction
        self.direction = pygame.math.Vector2()
        # Speed
        self.speed = 5

        # Attack variables
        # Flag
        self.attack = False
        # Cooldown
        self.attack_cooldown = 600
        # Time
        self.attack_time = None

        # Create weapon function reference
        self.create_weapon = create_weapon
        # Destroy weapon function reference
        self.destroy_weapon = destroy_weapon

        # Weapon variables
        # Current index
        self.weapon_index = 0
        # Current weapon
        self.weapon = list(settings.weapon_info.keys())[self.weapon_index]
        # Switch flag
        self.can_weapon_switch = True
        # Switch cooldown
        self.weapon_switch_cooldown = 350
        # Switch time
        self.weapon_switch_time = None

        # Player's stats
        self.stats = {"health": 100, "energy": 50, "attack": 10, "magic": 4, "speed": 5}
        # Current player's health and energy and speed
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        # Current player's experience
        self.exp = 120

    def update(self):
        """Update player's position"""
        # Update player's action
        self._handle_input()
        # Check the cooldowns
        self._cooldown()

        # Set state of the player
        self._set_state()
        # Animate the player
        self._animate()

        # Move the player
        self._move(self.speed)

    def _handle_input(self):
        """Set player's action based off input"""
        # If player is attacking, don't handle inputs
        if self.attack:
            return
        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.state = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.state = "right"
        else:
            self.direction.x = 0

        # Vertical movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.state = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.state = "down"
        else:
            self.direction.y = 0

        # Physical attack on K or Z
        if keys[pygame.K_k] or keys[pygame.K_z]:
            # Set attack flag to true and attack time to current one
            self.attack = True
            self.attack_time = pygame.time.get_ticks()
            self.create_weapon()
        # Magic attack on L or X
        elif keys[pygame.K_l] or keys[pygame.K_x]:
            # Magic flag and time is same as attack's
            self.attack = True
            self.attack_time = pygame.time.get_ticks()

        # Change weapon to the next one on F or Q
        if (keys[pygame.K_f] or keys[pygame.K_q]) and self.can_weapon_switch:
            # Make player unable to switch again
            self.can_weapon_switch = False
            # Get time of the switch
            self.weapon_switch_time = pygame.time.get_ticks()

            # If weapon index is still less than amount of weapons, increase it
            if self.weapon_index < len(list(settings.weapon_info.keys())) - 1:
                self.weapon_index += 1
            # Otherwise just reset it to 0
            else:
                self.weapon_index = 0
            # Change the weapon
            self.weapon = list(settings.weapon_info.keys())[self.weapon_index]

    def _move(self, speed):
        """Move the player"""
        # Normalize the direction if player moves, to prevent speed up
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move the player, check the collisions
        self.hitbox.x += self.direction.x * speed
        self._collision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self._collision("vertical")

        # Apply hitbox position
        self.rect.center = self.hitbox.center

    def _collision(self, direction):
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

    def _cooldown(self):
        """Manipulate the cooldowns"""
        current_time = pygame.time.get_ticks()

        # Handle player attack cooldown
        if self.attack:
            # If time from the last attack is bigger than the cooldown, allow to attack again
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attack = False
                self.destroy_weapon()
        # Handle weapon switch cooldown
        if not self.can_weapon_switch:
            # If the time between now and the last switch is bigger than the cooldown
            if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
                # Allow player to switch the weapon again
                self.can_weapon_switch = True

    def _import_assets(self):
        """Import player's assets"""
        # List of player's animations
        self.animations = {
            "up": [], "down": [], "left": [], "right": [], "right_idle": [], "left_idle": [],
            "up_idle": [], "down_idle": [], "right_attack": [], "left_attack": [], "up_attack": [],
            "down_attack": []
        }
        # Path to player's assets
        path = "../graphics/player"

        # Go through all the animations and import them
        for animation in self.animations.keys():
            full_path = path + '/' + animation
            self.animations[animation] = utilities.import_folder(full_path)

    def _set_state(self):
        """Set state of the player"""
        # If player isn't moving
        if self.direction.x == 0 and self.direction.y == 0:
            # If player's state isn't idle already, set it to the correct idle one
            if ("idle" not in self.state) and ("attack" not in self.state):
                self.state = self.state + "_idle"

        # If player is attacking
        if self.attack:
            # Stop him from moving
            self.direction.x, self.direction.y = 0, 0
            # If animation isn't attack one yet
            if "attack" not in self.state:
                # If it was idle, replace idle with attack to get correct attack direction
                if "idle" in self.state:
                    self.state = self.state.replace("idle", "attack")
                # Else - player just moved, just add attack to the direction
                else:
                    self.state = self.state + "_attack"
        # If player isn't attacking
        else:
            # If he was attacking before, remove the attack animation
            if "attack" in self.state:
                self.state = self.state.replace("attack", "idle")

    def _animate(self):
        """Animate the player"""
        # Get the current animation based off state
        animation = self.animations[self.state]

        # Move the frame
        self.frame += self.animation_speed
        # If the current frame is now higher than numbers of animation frames, reset it
        if self.frame >= len(animation):
            self.frame = 0

        # Set the image and update the rectangle
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
