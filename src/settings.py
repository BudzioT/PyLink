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

        # User's interface settings
        self.BAR_HEIGHT = 20
        self.FONT = "../graphics/font/joystix.ttf"
        self.FONT_SIZE = 18
        self.HEALTH_BAR_WIDTH = 200
        self.ENERGY_BAR_WIDTH = 140
        self.BOX_SIZE = 80
        # Colors
        self.BORDER_ACTIVE_COLOR = "yellow"
        self.HEALTH_COLOR = "red"
        self.ENERGY_COLOR = "blue"

        # General colors
        self.WATER_COLOR = "#71DDEE"
        self.BG_COLOR = "#222222"
        self.TEXT_COLOR = "#EEEEEE"
        self.BORDER_COLOR = "silver"

        # Weapon information
        self.weapon_info = {
            "rapier": {"cooldown": 70, "damage": 7, "graphic": "../graphics/weapons/rapier/full.png"},
            "sai": {"cooldown": 100, "damage": 10, "graphic": "../graphics/weapons/sai/full.png"},
            "sword": {"cooldown": 130, "damage": 13, "graphic": "../graphics/weapons/sword/full.png"},
            "lance": {"cooldown": 360, "damage": 20, "graphic": "../graphics/weapons/lance/full.png"},
            "axe": {"cooldown": 470, "damage": 28, "graphic": "../graphics/weapons/axe/full.png"}
        }

        # Information about magic
        self.magic_info = {
            "flame": {"strength": 5, "cost": 25, "graphic": "../graphics/particles/flame/fire.png"},
            "heal": {"strength": 15, "cost": 15, "graphic": "../graphics/particles/heal/heal.png"}
        }

        # Information about enemies
        self.enemy_info = {
            "squid": {"health": 100, "exp": 90, "damage": 22, "attack_type": "slash",
                      "attack_sound": "../audio/attack/slash.wav", "speed": 3, "resistance": 3,
                      "attack_radius": 80, "notice_radius": 360},
            "raccoon": {"health": 320, "exp": 250, "damage": 40, "attack_type": "claw",
                        "attack_sound": "../audio/attack/claw.wav", "speed": 2, "resistance": 2,
                        "attack_radius": 120, "notice_radius": 400},
            "spirit": {"health": 130, "exp": 110, "damage": 14, "attack_type": "fire",
                       "attack_sound": "../audio/attack/fireball.wav", "speed": 4, "resistance": 4,
                       "attack_radius": 90, "notice_radius": 420},
            "bamboo": {"health": 80, "exp": 90, "damage": 12, "attack_type": "leaf_attack",
                       "attack_sound": "../audio/attack/slash.wav", "speed": 3, "resistance": 3,
                       "attack_radius": 50, "notice_radius": 300},
        }


settings = Settings()
