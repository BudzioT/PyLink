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

    def update(self):
        """Update the enemy"""
        # Move the enemy
        self._move(self.speed)
        # Animate it
        self.animate()

    def enemy_update(self, player):
        """Update the enemy only, without other sprites"""
        # Get enemy's status
        self._set_state(player)
        # Make an action
        self.action(player)

    def action(self, player):
        """Make an action based off state"""
        if self.state == "attack":
            pass
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

    def _attack_cooldown(self):
        """Handle attack cooldown"""
        # If enemy can't attack, check the cooldown
        if not self.attack:
            # Get current time
            current_time = pygame.time.get_ticks()

    def _set_state(self, player):
        """Set state of the enemy"""
        # Get the distance from the player
        distance = self._get_position_from_player(player)[0]

        # If player is in enemy's attack radius, attack him if its able to
        if distance <= self.attack_radius and self.attack:
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
