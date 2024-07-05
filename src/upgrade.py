import pygame

from settings import settings


class UpgradeMenu:
    """Upgrade menu class"""
    def __init__(self, player):
        """Initialize the upgrade menu"""
        # Get main surface
        self.surface = pygame.display.get_surface()
        # Get the player
        self.player = player

        # Number of attributes
        self.attribute_number = len(player.stats)
        # Names of attributes
        self.attribute_names = list(player.stats.keys())

        # Max statistics values
        self.max_values = list(player.max_stats.values())

        # Font
        self.font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)

        # Dimensions of the items
        self.height = self.surface.get_height() * 0.7
        self.width = self.surface.get_width() // 6

        # Create the menu items
        self._create_items()

        # Current selected attribute index
        self.select_index = 0
        # Timer for selection
        self.select_time = None
        # Flag to be able to select attributes
        self.can_select = True

    def display(self):
        """Display the upgrade menu"""
        # Handle input
        self._handle_input()
        # Handle cooldown
        self._select_cooldown()

        # Draw the menu items
        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost(index)

            item.display(self.surface, self.select_index, name, value, max_value, cost)

    def _handle_input(self):
        """Handle the input"""
        # Get the keys pressed
        keys = pygame.key.get_pressed()

        # Check if player can select any of the options
        if self.can_select:
            # Move to the right option if players wants, check the index to not go too far
            if keys[pygame.K_RIGHT] or keys[pygame.K_a] and self.select_index < self.attribute_number:
                # Increase the selection index
                self.select_index += 1
                # Get select time
                self.select_time = pygame.time.get_ticks()
                # Stop the player from selecting too fast
                self.can_select = False

            # Move to left, make sure to not go under first option
            elif keys[pygame.K_LEFT] or keys[pygame.K_d] and self.select_index >= 1:
                # Decrease the selection index
                self.select_index -= 1
                self.select_time = pygame.time.get_ticks()
                self.can_select = False

            # Accept the selection
            if keys[pygame.K_SPACE]:
                self.select_time = pygame.time.get_ticks()
                self.can_select = False

    def _select_cooldown(self):
        """Handle the cooldown of attribute selection"""
        if not self.can_select:
            current_time = pygame.time.get_ticks()
            if current_time - self.select_time >= 400:
                self.can_select = True

    def _create_items(self):
        """Create selection items"""
        self.item_list = []

        for item_num, item_index in enumerate(range(self.attribute_number)):
            # Vertical position of the item
            top = self.surface.get_size()[1] * 0.15
            # Increment of the horizontal position (needed because there are several items)
            increment = self.surface.get_width() // self.attribute_number
            # Horizontal position of the item
            left = (item_num * increment) + (increment - self.width) // 2

            # Create the menu item
            item = Item(left, top, self.width, self.height, item_index, self.font)
            # Add it to the item list
            self.item_list.append(item)


class Item:
    """Singular menu item"""
    def __init__(self, left, top, width, height, index, font):
        """Initialize the menu item"""
        # Create the item's rectangle
        self.rect = pygame.Rect(left, top, width, height)
        # Store its index
        self.index = index
        # Save the font
        self.font = font

    def display(self, surface, selection_number, name, value, max_value, cost):
        """Display the item with certain information"""
        # Draw the background
        pygame.draw.rect(surface, settings.BG_COLOR, self.rect)

        # Display the text
        self.display_text(surface, name, cost, selection_number)

    def display_text(self, surface, name, cost, select):
        """Display all the text"""
        # Get statistic title text image and rectangle
        title_surface = self.font.render(name, False, settings.TEXT_COLOR)
        title_rect = title_surface.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        # Get its cost and cost's rect
        cost_surface = self.font.render(f"{int(cost)}", False, settings.TEXT_COLOR)

        # Draw the text
        surface.blit(title_surface, title_rect)
