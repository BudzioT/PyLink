from csv import reader
import os

import pygame

from settings import settings


class Utilities:
    """Utilities to help program"""
    def __init__(self):
        """Initialize utilities"""
        pass

    def import_csv_layout(self, path):
        """Import terrain as csv, return list with its content"""
        terrain = []

        # Open file, try to read it
        with open(os.path.join(settings.BASE_PATH, path)) as level:
            # Read CSV with delimiter that is ','
            layout = reader(level, delimiter=',')
            # Append every row of file into terrain list
            for row in layout:
                terrain.append(list(row))
            # Return the terrain list
            return terrain

    def import_folder(self, path):
        """Import files from a given directory path"""
        surfaces = []
        # Make the path absolute
        path = str(os.path.join(settings.BASE_PATH, path))

        # Go through each file that exists there
        for dir_path, dirs, images in os.walk(path):
            # Go through each of the images
            for image in images:
                # Save the full path to the image
                full_path = path + '/' + image
                # Load it
                image_surface = pygame.image.load(full_path).convert_alpha()
                surfaces.append(image_surface)
        return surfaces


utilities = Utilities()