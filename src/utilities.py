from csv import reader


class Utilities:
    """Utilities to help program"""
    def __init__(self):
        """Initialize utilities"""
        pass

    def import_csv_layout(self, path):
        """Import level as csv, return list with its content"""
        terrain = []

        # Open file, try to read it
        with open(path) as level:
            # Read CSV with delimiter that is ','
            layout = reader(level, delimiter=',')
            # Append every row of file into terrain list
            for row in layout:
                terrain.append(list(row))
            # Return the terrain list
            return terrain


utilities = Utilities()
