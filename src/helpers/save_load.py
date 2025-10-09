import json
import os

from .display import print_styled


def save_game(player, locations, console, settings):
    if not os.path.exists("saves"):
        os.makedirs("saves")

    # Build a dictionary of items in each location
    location_items = {}
    for location_id, location_data in locations.items():
        location_items[location_id] = location_data["items"]

    save_data = {
        "version": "0.0.1",
        "current_location": player.current_location,
        "active_quests": player.active_quests,
        "inventory": player.inventory,
        "location_items": location_items,
    }

    with open("saves/savegame.json", "w") as file:
        json.dump(save_data, file, indent=2)

    print_styled(console, settings, "Game succesfully saved.", style="green")


def load_game(console):
    if os.path.exists("saves/savegame.json"):
        with open("saves/savegame.json", "r") as file:
            save = json.load(file)
            return save
    return None
