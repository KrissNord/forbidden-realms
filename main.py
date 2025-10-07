import os
import sys
import time
from textwrap import dedent

import yaml
from rich.console import Console

from src.helpers.display import print_styled
from src.helpers.save_load import load_game, save_game
from src.helpers.validators import (validate_exits,
                                    validate_graph_connectivity, validate_npcs)

console = Console()

if os.path.exists("settings.yaml"):
    with open("settings.yaml", "r") as file:
        settings = yaml.safe_load(file)
else:
    settings = {
        "colors_enabled": True,
        "text_width": 90,
    }

location_files = os.listdir("data/locations/starting_locations/runewild_village/")
npc_files = os.listdir("data/npcs/starting_locations/runewild_village/")

locations = {}
for filename in location_files:
    if filename.endswith(".yaml"):
        location_id = filename.replace(".yaml", "")
        with open(
            f"data/locations/starting_locations/runewild_village/{filename}", "r"
        ) as file:
            location_data = yaml.safe_load(file)
        if location_data is not None:
            locations[location_id] = location_data
        else:
            print_styled(
                console,
                settings,
                f"Location file '{location_id}' is empty.",
                style="red",
            )

npcs = {}
for filename in npc_files:
    if filename.endswith(".yaml"):
        npc_id = filename.replace(".yaml", "")
        with open(
            f"data/npcs/starting_locations/runewild_village/{filename}", "r"
        ) as file:
            npc_data = yaml.safe_load(file)
            if npc_data is not None:
                npcs[npc_id] = npc_data
            else:
                print_styled(
                    console, settings, f"NPC file '{npc_id}' is empty.", style="red"
                )

loaded_location = load_game(console)
if loaded_location is not None:
    current_location_id = loaded_location
    console.clear()
    print_styled(console, settings, "Game loaded succesfully.", style="green")
    time.sleep(2)
else:
    current_location_id = "village_entrance"
    console.clear()
    print_styled(console, settings, "Starting new game.", style="cyan")
    time.sleep(2)
current_location = locations[current_location_id]

validate_graph_connectivity(locations, console, settings)

if validate_exits(locations, console, settings) and validate_npcs(
    locations, npcs, console, settings
):

    console.clear()
    with open("data/ascii/title.txt", "r") as file:
        content = file.read()
        print_styled(console, settings, content, style="cyan", wrap=False)
    console.print()
    print_styled(console, settings, current_location["name"], style="bold cyan")
    print_styled(console, settings, current_location["short_description"])

    while True:
        command = console.input("[bold white]> [/bold white]")

        parts = command.split()
        if len(parts) >= 2:
            action = parts[0]
            if action == "go":
                direction = parts[1]
                if direction in current_location["exits"]:
                    current_location_id = current_location["exits"][direction]
                    current_location = locations[current_location_id]
                    print_styled(
                        console, settings, current_location["name"], style="bold cyan"
                    )
                    print_styled(
                        console, settings, current_location["short_description"]
                    )
            elif action == "talk":
                name_parts = parts[1:]
                name_id = "_".join(name_parts)
                full_name = " ".join(name_parts)
                if name_id in current_location["npcs"]:
                    print_styled(
                        console, settings, npcs[name_id]["name"], style="bold yellow"
                    )
                    print_styled(
                        console,
                        settings,
                        npcs[name_id]["greeting_message"],
                        style="green",
                    )
                else:
                    print_styled(
                        console,
                        settings,
                        f"There is no one named {full_name.title()} around here.",
                        style="red",
                    )
        elif command == "quit":
            break
        elif command == "look":
            print_styled(
                console,
                settings,
                current_location["detailed_description"],
                style="bright_white",
            )
        elif command == "save":
            save_game(current_location_id, console, settings)
        elif command == "help":
            print_styled(
                console,
                settings,
                dedent(
                    """
            Available Commands:
                look - View detailed description of current location.
                go [direction] - Move in a direction (north, south, east, west).
                help - Show this help message.
                quit - Exit the game.
            """
                ),
                style="blue",
            )
        else:
            print_styled(console, settings, command)

else:
    print_styled(console, settings, "Validation failed.", style="red")
    sys.exit()
