"""
Character Creator for Forbidden Realms

This module handles the sequential character creation flow:
1. Name input
2. Race selection
3. Class selection
4. Background selection
5. Stats preview and confirmation
"""

from rich.panel import Panel


def get_character_name(console, settings, print_styled):
    """
    Prompt the player to enter their character name.

    Requirements:
    - Name must not be empty
    - Name should be 2-20 characters
    - If invalid, ask again

    Returns:
        str: The validated character name
    """
    console.clear()
    print_styled(console, settings, "=== Character Creation ===\n", style="bold cyan")
    print_styled(console, settings, "What is your name, adventurer?", style="cyan")

    while True:
        name = console.input("[bold white]> [/bold white]").strip()

        # TODO: Validate name
        # - Check if empty
        # - Check length (2-20 chars)
        # - If valid, return name
        # - If invalid, print error and loop again
        if not name:

        pass  # Remove this when you add your code


def choose_race(races_dict, console, settings, print_styled):
    """
    Display race options and let player choose.

    Requirements:
    - Show numbered list of races with descriptions
    - Get player input
    - Validate choice (must be valid number)
    - Return the race_id

    Args:
        races_dict: Dictionary of race data loaded from YAML

    Returns:
        str: The chosen race_id (e.g., "human", "elf")
    """
    console.clear()
    print_styled(console, settings, "=== Choose Your Race ===\n", style="bold cyan")

    # TODO: Create a list from races_dict keys
    # Hint: race_list = list(races_dict.keys())

    # TODO: Loop through race_list with enumerate(start=1)
    # For each race, print:
    #   - Number
    #   - Race name (from race_data["name"])
    #   - Race description
    # Make it look nice!

    console.print()

    while True:
        choice = console.input("[bold cyan]Choose (1-?): [/bold cyan]")

        # TODO: Validate choice
        # - Try to convert to int
        # - Check if in valid range
        # - If valid, return race_list[choice_num - 1]
        # - If invalid, print error and loop again

        pass  # Remove this when you add your code


def choose_class(classes_dict, console, settings, print_styled):
    """
    Display class options and let player choose.

    Follow the same pattern as choose_race(), but for classes.
    Show the class name, description, and maybe the playstyle.

    Returns:
        str: The chosen class_id (e.g., "warrior", "mage")
    """
    console.clear()
    print_styled(console, settings, "=== Choose Your Class ===\n", style="bold cyan")

    # TODO: Implement this following the same pattern as choose_race()
    # You can copy and modify the structure

    pass


def choose_background(backgrounds_dict, console, settings, print_styled):
    """
    Display background options and let player choose.

    Follow the same pattern as choose_race(), but for backgrounds.

    Returns:
        str: The chosen background_id (e.g., "soldier", "scholar")
    """
    console.clear()
    print_styled(console, settings, "=== Choose Your Background ===\n", style="bold cyan")

    # TODO: Implement this following the same pattern

    pass


def show_character_preview(player, race_data, class_data, background_data, console, settings, print_styled):
    """
    Display the character's final stats and ask for confirmation.

    Show:
    - Name, race, class, background
    - All 7 primary stats
    - Important secondary stats (HP, Mana, Attack, etc.)

    Returns:
        bool: True if player confirms, False if they want to restart
    """
    console.clear()
    print_styled(console, settings, "=== Your Character ===\n", style="bold cyan")

    # TODO: Display character info
    # Hint: Use player.name, player.race, player.character_class, player.background
    # Hint: Use player.get_strength(race_data, class_data, background_data) for stats

    # TODO: Show all 7 primary stats

    # TODO: Show key secondary stats (HP, Mana, Stamina, Attack)

    console.print()
    print_styled(console, settings, "Confirm this character? (yes/no)", style="yellow")

    while True:
        choice = console.input("[bold white]> [/bold white]").strip().lower()

        # TODO: Handle yes/no
        # - If "yes" or "y", return True
        # - If "no" or "n", return False
        # - Otherwise, ask again

        pass


def create_character(player, races, classes, backgrounds, console, settings, print_styled):
    """
    Main character creation flow.

    This function orchestrates the entire process:
    1. Get name
    2. Choose race
    3. Choose class
    4. Choose background
    5. Preview and confirm
    6. Apply choices to player object

    Args:
        player: The Player object to configure
        races: Dictionary of race data
        classes: Dictionary of class data
        backgrounds: Dictionary of background data
    """

    while True:  # Loop allows restarting if player doesn't confirm
        # TODO: Step 1 - Get character name
        # Hint: name = get_character_name(console, settings, print_styled)

        # TODO: Step 2 - Choose race
        # Hint: race_id = choose_race(races, console, settings, print_styled)

        # TODO: Step 3 - Choose class

        # TODO: Step 4 - Choose background

        # TODO: Apply choices to player object
        # Hint: player.name = name
        # Hint: player.race = race_id
        # etc.

        # TODO: Get the data dictionaries for preview
        # Hint: race_data = races[player.race]

        # TODO: Step 5 - Show preview and get confirmation
        # Hint: confirmed = show_character_preview(player, race_data, class_data, background_data, ...)

        # TODO: If confirmed, apply starting items and initialize stats
        # Hint: player.initialize_current_stats(race_data, class_data, background_data)
        # Hint: Add starting items from class_data["starting_items"]
        # Hint: Set starting gold from background_data["starting_gold"]

        # TODO: If confirmed, break the loop
        # If not confirmed, loop restarts

        pass
