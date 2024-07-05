from random import choice

import pygame

from utilities import utilities


class Particle(pygame.sprite.Sprite):
    """Particle effect class"""
    def __init__(self, pos, group, frames, sprite_type=None):
        """Initialize the particle"""
        super().__init__(group)

        # Available frames and the current frame
        self.frames = frames
        self.frame = 0
        # Animation speed
        self.animation_speed = 0.15
        # Image based off current frame
        self.image = self.frames[self.frame]
        # Rectangle of particle
        self.rect = self.image.get_rect(center=pos)

        # Sprite type
        self.sprite_type = "magic"

    def update(self):
        """Update the particle"""
        self.animate()

    def animate(self):
        """Animate the particle"""
        # Increase the frame
        self.frame += self.animation_speed
        # If frames ended, kill the particle
        if self.frame >= len(self.frames):
            self.kill()
        # Otherwise set the image to the current frame
        else:
            self.image = self.frames[int(self.frame)]


class Animation:
    """Class for loading animations"""
    def __init__(self):
        """Initialize animation"""
        # Load and store all the animations, that aren't loaded already
        self.frames = {}
        self._load_frames()

        # Increase shield size by 3 times
        for num in range(len(self.frames["shield"])):
            frame = self.frames["shield"][num]
            self.frames["shield"][num] = pygame.transform.scale(frame, (frame.get_rect().width * 3,
                                                                        frame.get_rect().height * 3))

        # Increase energy ball size by 4 times
        for num in range(len(self.frames["energy_ball"])):
            frame = self.frames["energy_ball"][num]
            self.frames["energy_ball"][num] = pygame.transform.scale(frame, (frame.get_rect().width * 4,
                                                                        frame.get_rect().height * 4))

    def grass_particles(self, pos, group):
        """Create grass particles, animate them"""
        # Get random leaf animation type
        animation_frames = choice(self.frames["leaf"])
        # Create the particle animation
        Particle(pos, group, animation_frames)

    def create_particles(self, attack_type, pos, group):
        """Create and animate particles"""
        # Get animation type based off attack type
        animation_frames = self.frames[attack_type]
        # Create particle animation
        Particle(pos, group, animation_frames)

    def reflect_images(self, frames):
        """Reflect the images"""
        flipped_frames = []

        # Go through each frame
        for frame in frames:
            # Flip it at X-Axis, append it to the list
            flipped = pygame.transform.flip(frame, True, False)
            flipped_frames.append(flipped)
        # Return all the flipped images
        return flipped_frames

    def _load_frames(self):
        """Load all the frames and add it to the dictionary"""
        self.frames = {
            # Attacks
            "claw": utilities.import_folder("../graphics/particles/claw"),
            "slash": utilities.import_folder("../graphics/particles/slash"),
            "thunder": utilities.import_folder("../graphics/particles/thunder"),
            "leaf_attack": utilities.import_folder("../graphics/particles/leaf_attack"),
            "sparkle": utilities.import_folder("../graphics/particles/sparkle"),

            # Player's magic
            "flame": utilities.import_folder("../graphics/particles/flame/frames"),
            "heal": utilities.import_folder("../graphics/particles/heal/frames"),
            "aura": utilities.import_folder("../graphics/particles/aura"),
            "energy_ball": utilities.import_folder("../graphics/particles/energy_ball/frames"),
            "shield": utilities.import_folder("../graphics/particles/shield/frames"),

            # Monster kill
            "squid": utilities.import_folder("../graphics/particles/smoke_orange"),
            "spirit": utilities.import_folder("../graphics/particles/nova"),
            "raccoon": utilities.import_folder("../graphics/particles/raccoon"),
            "bamboo": utilities.import_folder("../graphics/particles/bamboo"),

            # Leafs
            "leaf": (
                utilities.import_folder("../graphics/particles/leaf1"),
                utilities.import_folder("../graphics/particles/leaf2"),
                utilities.import_folder("../graphics/particles/leaf3"),
                utilities.import_folder("../graphics/particles/leaf4"),
                utilities.import_folder("../graphics/particles/leaf5"),
                utilities.import_folder("../graphics/particles/leaf6"),
                # Reflected ones, for smooth animation
                self.reflect_images(utilities.import_folder("../graphics/particles/leaf1")),
                self.reflect_images(utilities.import_folder("../graphics/particles/leaf2")),
                self.reflect_images(utilities.import_folder("../graphics/particles/leaf3")),
                self.reflect_images(utilities.import_folder("../graphics/particles/leaf4")),
                self.reflect_images(utilities.import_folder("../graphics/particles/leaf5")),
                self.reflect_images(utilities.import_folder("../graphics/particles/leaf6"))
            )
        }
