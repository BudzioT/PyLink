import os


class Settings:
    """Settings of the game"""
    def __init__(self):
        """Initialize settings"""
        # Dimensions of the game
        self.WIDTH = 1280
        self.HEIGHT = 720
        # FPS
        self.FPS = 60
        # One tile size
        self.SIZE = 64

        # Base file path
        self.BASE_PATH = os.path.dirname(os.path.abspath(__file__))

        # Weapon information
        self.weapon_info = {
            "rapier": {"cooldown": 70, "damage": 7, "graphic": "../graphics/weapons/rapier/full.png"},
            "sai": {"cooldown": 100, "damage": 10, "graphic": "../graphics/weapons/sai/full.png"},
            "sword": {"cooldown": 130, "damage": 13, "graphic": "../graphics/weapons/sword/full.png"},
            "lance": {"cooldown": 360, "damage": 20, "graphic": "../graphics/weapons/lance/full.png"},
            "axe": {"cooldown": 470, "damage": 28, "graphic": "../graphics/weapons/axe/full.png"}
        }


settings = Settings()