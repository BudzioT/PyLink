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


settings = Settings()