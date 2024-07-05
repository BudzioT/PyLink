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
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.select_index < self.attribute_number - 1:
                # Increase the selection index
                self.select_index += 1
                # Get select time
                self.select_time = pygame.time.get_ticks()
                # Stop the player from selecting too fast
                self.can_select = False

            # Move to left, make sure to not go under first option
            elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.select_index >= 1:
                # Decrease the selection index
                self.select_index -= 1
                self.select_time = pygame.time.get_ticks()
                self.can_select = False

            # Accept the selection
            if keys[pygame.K_SPACE]:
                self.select_time = pygame.time.get_ticks()
                self.can_select = False
                # Trigger item, try to upgrade statistics of the player
                self.item_list[self.select_index].trigger(self.player)

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
        # Draw lighter background when user selected this item
        if self.index == selection_number:
            pygame.draw.rect(surface, settings.UPGRADE_SELECT_BG_COLOR, self.rect)
            pygame.draw.rect(surface, settings.BORDER_COLOR, self.rect, 4)
        # Otherwise draw normal background
        else:
            pygame.draw.rect(surface, settings.BG_COLOR, self.rect)
            pygame.draw.rect(surface, settings.BORDER_COLOR, self.rect, 4)

        # User selected this item flag
        select = self.index == selection_number

        # Display the text
        self.display_text(surface, name, cost, select)
        # Display the progress bar
        self.display_bar(surface, value, max_value, select)

    def display_text(self, surface, name, cost, select):
        """Display all the text"""
        # Set the text color depending on, if player selected this option
        text_color = settings.TEXT_SELECT_COLOR if select else settings.TEXT_COLOR

        # Get statistic title text image and rectangle
        title_surface = self.font.render(name, False, text_color)
        title_rect = title_surface.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        # Get its cost and cost's rect
        cost_surface = self.font.render(f"{int(cost)}", False, text_color)
        cost_rect = cost_surface.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))

        # Draw the text
        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)

    def display_bar(self, surface, value, max_value, select):
        """Display the bar of upgrade progress"""
        # Set the bar's dimensions
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        # Set the color based off the selection
        color = settings.BAR_SELECT_COLOR if select else settings.BAR_COLOR

        height = bottom[1] - top[1]
        progress = (value / max_value) * height
        progress_rect = pygame.Rect(top[0] - 15, bottom[1] - progress, 30, 10)

        # Draw the progress line
        pygame.draw.line(surface, color, top, bottom, 5)
        # Draw the progress rectangle
        pygame.draw.rect(surface, color, progress_rect)

    def trigger(self, player):
        """Trigger the item"""
        # Get the statistic that player wants to upgrade
        upgrade = list(player.stats.keys())[self.index]

        # If player has enough experience points and his stat isn't at max value already, upgrade the stat
        if player.exp >= player.upgrade_cost[upgrade] and player.stats[upgrade] < player.max_stats[upgrade]:
            # Decrease his experience points
            player.exp -= player.upgrade_cost[upgrade]
            # Upgrade his stat by 1.15
            player.stats[upgrade] *= 1.15
            # Increase the next upgrade cost of this stat by 1.45
            player.upgrade_cost[upgrade] *= 1.45

            # Don't allow the player to exceed the max value of the stat
            if player.stats[upgrade] > player.max_stats[upgrade]:
                player.stats[upgrade] = player.max_stats[upgrade]
