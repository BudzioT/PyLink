import pygame

from settings import settings
from entity import Entity
from utilities import utilities


class Enemy(Entity):
    """Enemy class"""
    def __init__(self, name, pos, group, object_sprites, damage_player, death_particles, increase_exp):
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

        # Get enemies information dictionary
        enemy_info = settings.enemy_info[name]
        # Enemy statistics
        self.name = name
        # General stats
        self.exp = enemy_info["exp"]
        self.speed = enemy_info["speed"]
        # Defense stats
        self.health = enemy_info["health"]
        self.resistance = enemy_info["resistance"]
        # Attack stats
        self.attack_type = enemy_info["attack_type"]
        self.attack_damage = enemy_info["damage"]
        # Radius stats
        self.attack_radius = enemy_info["attack_radius"]
        self.notice_radius = enemy_info["notice_radius"]

        # Attack flag
        self.attack = True
        # Attack timer and cooldown
        self.attack_time = None
        self.attack_cooldown = 400

        # Vulnerability flag
        self.vulnerable = True
        # Last time getting hit
        self.hit_time = None
        # Duration of the invincibility
        self.dodge_duration = 350

        # Get the function to damage player
        self.damage_player = damage_player
        # And to increase his exp
        self.increase_exp = increase_exp

        # Get the function reference to trigger particles on death
        self.death_particles = death_particles

    def update(self):
        """Update the enemy"""
        # React on getting hit
        self.react_on_damage()

        # Move the enemy
        self._move(self.speed)
        # Animate it
        self.animate()

        # Check attack cooldown
        self._attack_cooldown()

        # Check and handle death
        self.death()

    def enemy_update(self, player):
        """Update the enemy only, without other sprites"""
        # Get enemy's status
        self._set_state(player)
        # Make an action
        self.action(player)

    def action(self, player):
        """Make an action based off state"""
        # Attack the player
        if self.state == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        # Move closer to the player
        elif self.state == "move":
            self.direction = self._get_position_from_player(player)[1]
        # Don't do anything
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        """Animate the enemy"""
        # Get the animation list based off current state
        animation = self.animations[self.state]

        # Increase the frame based off animation speed
        self.frame += self.animation_speed

        # If current frame is out of bound, return it to 0
        if self.frame >= len(animation):
            # If enemy's attacking, don't allow him to do this repeatable
            if self.state == "attack":
                self.attack = False
            self.frame = 0

        # Set the current frame's image
        self.image = animation[int(self.frame)]
        # Update the enemy's rect
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # If enemy can't be hit, meaning it got hit earlier
        if not self.vulnerable:
            # Set the alpha based off current time's sinus
            self.image.set_alpha(self.wave_value())
        # Otherwise just set the image to normal
        else:
            self.image.set_alpha(255)

    def get_damage(self, player, attack_type):
        """Get damage when hit by the player"""
        # If enemy can be hit
        if self.vulnerable:
            # Get the direction based off player's position from the enemy
            self.direction = self._get_position_from_player(player)[1]

            # If enemy was hit by a weapon, get damaged from it
            if attack_type == "weapon":
                self.health -= player.get_weapon_damage()
            # Otherwise deal the damage from a magic
            else:
                self.health -= player.get_magic_damage()

            # Save the last hit's time
            self.hit_time = pygame.time.get_ticks()
            # Block the player from hitting the enemy right again
            self.vulnerable = False

    def death(self):
        """Check for death and handle it"""
        if self.health <= 0:
            # Kill the enemy
            self.kill()

            # Add experience points for the player
            self.increase_exp(self.exp)

            # Create particles
            self.death_particles(self.rect.center, self.name)

    def react_on_damage(self):
        """React when getting damaged"""
        # If enemy isn't vulnerable anymore, push it back
        if not self.vulnerable:
            # Change direction by negative resistance, meaning a push back
            self.direction *= -self.resistance

    def _attack_cooldown(self):
        """Handle attack cooldown"""
        # Get current time
        current_time = pygame.time.get_ticks()

        # If enemy can't attack, check the cooldown
        if not self.attack:
            # If cooldown has passed, allow enemy to attack again
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attack = True
        # If enemy isn't vulnerable, check the cooldown again
        if not self.vulnerable:
            # If cooldown has passed, make the enemy vulnerable
            if current_time - self.hit_time >= self.dodge_duration:
                self.vulnerable = True

    def _set_state(self, player):
        """Set state of the enemy"""
        # Get the distance from the player
        distance = self._get_position_from_player(player)[0]

        # If player is in enemy's attack radius, attack him if its able to
        if distance <= self.attack_radius and self.attack:
            # If enemy didn't attack yet, set the frame to 0
            if self.state != "attack":
                self.frame = 0
            # Set the state  to attack
            self.state = "attack"
        # If player is in enemy's notice radius, move after him
        elif distance <= self.notice_radius:
            self.state = "move"
        # Otherwise just idle
        else:
            self.state = "idle"

    def _get_position_from_player(self, player):
        """Calculate distance between the enemy and player"""
        # Save enemy's and player's position as a 2D vector
        enemy_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)

        # Calculate the distance, magnitude it, to get the length
        distance = (player_pos - enemy_pos).magnitude()
        # Normalize the difference of positions to get the direction
        if distance > 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def _import_graphics(self, name):
        """Import assets of enemy based off name"""
        self.animations = {"idle": [], "move": [], "attack": []}
        path = f"../graphics/monsters/{name}/"

        # Go through each type of animations
        for animation in self.animations.keys():
            # Import the current animation pack to the list in dictionary
            self.animations[animation] = utilities.import_folder(path + animation)
