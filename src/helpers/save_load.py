import json
import os

from .display import print_styled


def save_game(current_location_id, console, settings):
    if not os.path.exists("saves"):
        os.makedirs("saves")

    save_data = {
        "version": "0.0.1",
        "current_location_id": current_location_id,
    }

    with open("saves/savegame.json", "w") as file:
        json.dump(save_data, file, indent=2)

    print_styled(console, settings, "Game succesfully saved.", style="green")


def load_game(console):
    if os.path.exists("saves/savegame.json"):
        with open("saves/savegame.json", "r") as file:
            save = json.load(file)
            return save["current_location_id"]
