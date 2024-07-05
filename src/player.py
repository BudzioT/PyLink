import os

import pygame

from settings import settings
from utilities import utilities
from entity import Entity


class Player(Entity):
    """Player class"""
    def __init__(self, pos, group, object_sprites, create_weapon, destroy_weapon,
                 create_magic, destroy_magic):
        super().__init__(group)

        # Load player's image and get its rect
        self.image = pygame.image.load(os.path.join(settings.BASE_PATH,
                                                    "../graphics/test/player.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # Import player's assets
        self._import_assets()
        # Set player's state
        self.state = "down"

        # Hitbox of the player
        self.hitbox = self.rect.inflate(0, -26)

        # Get object sprites
        self.object_sprites = object_sprites

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

        # Create and destroy magic function references
        self.create_magic = create_magic
        self.destroy_magic = destroy_magic

        # Weapon variables
        # Current index
        self.weapon_index = 0
        # Current weapon
        self.weapon = list(settings.weapon_info.keys())[self.weapon_index]
        # Switch flag
        self.can_weapon_switch = True
        # Switch cooldown
        self.weapon_switch_cooldown = 400
        # Switch time
        self.weapon_switch_time = None

        # Magic variables
        # Current index
        self.magic_index = 0
        # List of magic spells
        self.magic = list(settings.magic_info.keys())[self.magic_index]
        # Switch flag
        self.can_magic_switch = True
        # Spell switching cooldown
        self.magic_switch_cooldown = 500
        # Last magic used time
        self.magic_switch_time = None

        # Player's stats
        self.stats = {"health": 100, "energy": 50, "attack": 10, "magic": 4, "speed": 5}
        # Current player's health and energy and speed
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        # Current player's experience
        self.exp = 120

        # Vulnerability flag
        self.vulnerable = True
        # Last hit's time
        self.hit_time = None
        # Duration of dodges
        self.dodge_duration = 500

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

        # Recover the energy
        self._recover_energy()

        # Move the player
        self._move(self.speed)

    def get_weapon_damage(self):
        """Get the damage that weapon's deal"""
        # Return damage dealt by specific weapon
        return self.stats["attack"] + settings.weapon_info[self.weapon]["damage"]

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

            # Get magic's style (name), strength and cost
            style = list(settings.magic_info.keys())[self.magic_index]
            strength = settings.magic_info[style]["strength"] + self.stats["magic"]
            cost = settings.magic_info[style]["strength"]

            # Create the magic
            self.create_magic(style, strength, cost)

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

        # Change magic with E or C
        if (keys[pygame.K_e] or keys[pygame.K_c]) and self.can_magic_switch:
            # Change player's ability to change magic to False, save the time
            self.can_magic_switch = False
            self.magic_switch_time = pygame.time.get_ticks()

            # If index is still in bound, increment it
            if self.magic_index < len(list(settings.magic_info.keys())) - 1:
                self.magic_index += 1
            # Otherwise move it down to 0
            else:
                self.magic_index = 0
            # Change the magic
            self.magic = list(settings.magic_info.keys())[self.magic_index]

    def _cooldown(self):
        """Manipulate the cooldowns"""
        current_time = pygame.time.get_ticks()

        # Handle player attack cooldown
        if self.attack:
            # Calculate the cooldown by adding base one to the weapon one
            cooldown = self.attack_cooldown + settings.weapon_info[self.weapon]["cooldown"]
            # If time from the last attack is bigger than the cooldown, allow to attack again
            if current_time - self.attack_time >= cooldown:
                self.attack = False
                self.destroy_weapon()

        # Handle weapon switch cooldown
        if not self.can_weapon_switch:
            # If the time between now and the last switch is bigger than the cooldown
            if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
                # Allow player to switch the weapon again
                self.can_weapon_switch = True

        # Handle magic switch cooldown
        if not self.can_magic_switch:
            # If magic cooldown has passed, allow the player to use it again
            if current_time - self.magic_switch_time >= self.magic_switch_cooldown:
                self.can_magic_switch = True

        # Handle vulnerability cooldown
        if not self.vulnerable:
            # If invincibility cooldown is over, make player vulnerable again
            if current_time - self.hit_time >= self.dodge_duration:
                self.vulnerable = True

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

    def _recover_energy(self):
        """Handle recovering energy"""
        # Recover the energy if it's not full yet
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        # Otherwise just keep it full
        else:
            self.energy = self.stats["energy"]

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

        # If player just got hit, meaning he isn't vulnerable
        if not self.vulnerable:
            # Set the alpha to current sinus value
            self.image.set_alpha(self.wave_value())
        # Otherwise set it to normal
        else:
            self.image.set_alpha(255)
