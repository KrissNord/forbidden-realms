import os
import sys
import time
from textwrap import dedent

import yaml
from rich.console import Console
from rich.panel import Panel

from src.character.player import Player
from src.helpers.display import print_styled
from src.helpers.save_load import load_game, save_game
from src.helpers.validators import (validate_exits,
                                    validate_graph_connectivity, validate_items,
                                    validate_npcs)

console = Console()
player = Player()

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
quest_files = os.listdir("data/quests/starting_locations/runewild_village")

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

quests = {}
for filename in quest_files:
    if filename.endswith(".yaml"):
        quest_id = filename.replace(".yaml", "")
        with open(
            f"data/quests/starting_locations/runewild_village/{filename}", "r"
        ) as file:
            quest_data = yaml.safe_load(file)
        if quest_data is not None:
            quests[quest_id] = quest_data

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

# Load items
items = {}
item_files = os.listdir("data/items/")
for filename in item_files:
    if filename.endswith(".yaml"):
        item_id = filename.replace(".yaml", "")
        with open(f"data/items/{filename}", "r") as file:
            item_data = yaml.safe_load(file)
            if item_data is not None:
                items[item_id] = item_data
            else:
                print_styled(
                    console, settings, f"Item file '{item_id}' is empty.", style="red"
                )

loaded_data = load_game(console)
if loaded_data is not None:
    player.current_location = loaded_data["current_location"]
    player.active_quests = loaded_data["active_quests"]
    player.inventory = loaded_data["inventory"]

    if "location_items" in loaded_data:
        for location_id, items in loaded_data["location_items"].items():
            if location_id in locations:
                locations[location_id]["items"] = items

    console.clear()
    print_styled(console, settings, "Game loaded succesfully.", style="green")
    time.sleep(2)
else:
    console.clear()
    print_styled(console, settings, "Starting new game.", style="cyan")
    time.sleep(2)
current_location = locations[player.current_location]

validate_graph_connectivity(locations, console, settings)

if (
    validate_exits(locations, console, settings)
    and validate_npcs(locations, npcs, console, settings)
    and validate_items(locations, items, console, settings)
):

    console.clear()
    with open("data/ascii/title.txt", "r") as file:
        content = file.read()
        print_styled(console, settings, content, style="cyan", wrap=False)
    console.print()
    print_styled(
        console,
        settings,
        current_location["name"],
        style="bold cyan",
    )
    print_styled(
        console,
        settings,
        current_location["short_description"],
    )

    while True:
        command = console.input("[bold white]> [/bold white]")

        parts = command.split()
        if len(parts) >= 2:
            action = parts[0]
            if action == "go":
                direction = parts[1]
                if direction in current_location["exits"]:
                    new_location_id = current_location["exits"][direction]
                    player.current_location = new_location_id
                    current_location = locations[new_location_id]
                    console.clear()
                    entry_content = f"[bright_white]{current_location['short_description']}[/bright_white]\n\n"

                    if current_location["npcs"]:
                        npc_names = [
                            npcs[npc]["name"] for npc in current_location["npcs"]
                        ]
                        entry_content += f"[bold yellow]People:[/bold yellow] {', '.join(npc_names)}\n"

                    exit_directions = ", ".join(current_location["exits"].keys())
                    entry_content += (
                        f"[bold yellow]Exits:[/bold yellow] {exit_directions}"
                    )

                    console.print(
                        Panel(
                            entry_content,
                            title=f"[bold cyan]{current_location['name']}[/bold cyan]",
                            border_style="cyan",
                        )
                    )
            elif action == "take":
                item_parts = parts[1:]
                item_input = "_".join(item_parts)

                if item_input in current_location["items"]:
                    current_location["items"].remove(item_input)
                    player.inventory.append(item_input)

                    # Get item name from loaded data or fallback to formatted ID
                    item_name = items[item_input]["name"] if item_input in items else item_input.replace("_", " ").title()
                    print_styled(
                        console,
                        settings,
                        f"{item_name} added to inventory.",
                        style="green",
                    )

                else:
                    item_name = items[item_input]["name"] if item_input in items else item_input.replace("_", " ")
                    print_styled(
                        console,
                        settings,
                        f"There is no {item_name} around here.",
                        style="red",
                    )
            elif action == "use":
                item_parts = parts[1:]
                item_input = "_".join(item_parts)

                if item_input in player.inventory:
                    player.inventory.remove(item_input)

                    # Get item name from loaded data or fallback to formatted ID
                    item_name = items[item_input]["name"] if item_input in items else item_input.replace("_", " ").title()
                    print_styled(
                        console,
                        settings,
                        f"You used the {item_name}.",
                        style="green",
                    )
                else:
                    print_styled(
                        console,
                        settings,
                        "You don't have that item.",
                        style="red",
                    )
            elif action == "inspect":
                item_parts = parts[1:]
                item_input = "_".join(item_parts)

                # Check if item is in inventory or current location
                if item_input in player.inventory or item_input in current_location["items"]:
                    if item_input in items:
                        item_data = items[item_input]

                        # Build content for panel
                        content = f"[bright_white]{item_data['description']}[/bright_white]\n\n"
                        content += f"[bold yellow]Type:[/bold yellow] {item_data['type'].capitalize()}\n"
                        content += f"[bold yellow]Value:[/bold yellow] {item_data['value']} gold\n"
                        content += f"[bold yellow]Weight:[/bold yellow] {item_data['weight']} lbs\n"
                        content += f"[bold yellow]Rarity:[/bold yellow] {item_data['rarity'].capitalize()}"

                        console.print(
                            Panel(
                                content,
                                title=f"[bold cyan]{item_data['name']}[/bold cyan]",
                                border_style="cyan",
                            )
                        )
                    else:
                        # Item exists but no YAML file
                        item_name = item_input.replace("_", " ").title()
                        print_styled(
                            console,
                            settings,
                            f"You examine the {item_name}, but there's nothing special about it.",
                            style="yellow",
                        )
                else:
                    item_name = items[item_input]["name"] if item_input in items else item_input.replace("_", " ")
                    print_styled(
                        console,
                        settings,
                        f"You don't see any {item_name} here.",
                        style="red",
                    )
            elif action == "talk":
                name_parts = parts[1:]
                name_id = "_".join(name_parts)
                full_name = " ".join(name_parts)
                if name_id in current_location["npcs"]:
                    current_node = "greeting"

                    while True:
                        node_data = npcs[name_id]["dialogues"][current_node]

                        print_styled(
                            console,
                            settings,
                            npcs[name_id]["name"],
                            style="bold yellow",
                        )
                        print_styled(
                            console, settings, node_data["text"], style="green"
                        )
                        console.print()
                        if "trigger_quest" in node_data:
                            quest_id = node_data["trigger_quest"]

                            player.active_quests[quest_id] = {"status": "active"}

                            console.print("[cyan]New quest accepted![/cyan]")

                        for index, choice in enumerate(node_data["choices"], start=1):
                            print_styled(
                                console,
                                settings,
                                f"{index}. {choice['text']}",
                                style="blue",
                            )
                        if len(node_data["choices"]) == 0:
                            break

                        try:
                            console.print()
                            user_input = console.input("[bold cyan]> [/]")
                            choice_num = int(user_input)

                            selected_choice = node_data["choices"][choice_num - 1]
                            next_node = selected_choice["goes_to"]

                            current_node = next_node
                        except:
                            print_styled(
                                console,
                                settings,
                                "Invalid choice, please try again.",
                                style="red",
                            )
                            continue
                else:
                    print_styled(
                        console,
                        settings,
                        f"There is no one named {full_name.title()} around here.",
                        style="red",
                    )
        elif command == "quit":
            break
        elif command == "inventory":
            console.clear()
            if len(player.inventory) == 0:
                print_styled(
                    console, settings, "Your inventory is empty.", style="yellow"
                )
            else:
                print_styled(console, settings, "=== Inventory ===", style="cyan")
                for item in player.inventory:
                    # Get item name from loaded data or fallback to formatted ID
                    item_name = items[item]["name"] if item in items else item.replace("_", " ").title()
                    print_styled(
                        console, settings, f" • {item_name}"
                    )
                if len(player.inventory) == 1:
                    print_styled(
                        console,
                        settings,
                        f"\n\nYou are carrying {len(player.inventory)} item.",
                        style="green",
                    )
                else:
                    print_styled(
                        console,
                        settings,
                        f"\n\nYou are carrying {len(player.inventory)} items.",
                        style="green",
                    )
        elif command == "look":
            console.clear()
            content = f"[bright_white]{current_location['detailed_description']}[/bright_white]\n\n"

            if current_location["npcs"]:
                content += "[bold yellow]People here:[/bold yellow]\n"
                for npc in current_location["npcs"]:
                    npc_name = npcs[npc]["name"]
                    content += f"   • {npc_name}\n"

                content += "\n"

            if current_location["items"]:
                content += f"[bold yellow]Items here:[/bold yellow]\n"
                for item in current_location["items"]:
                    # Get item name from loaded data or fallback to formatted ID
                    item_display = items[item]["name"] if item in items else item.replace("_", " ").title()
                    content += f"   • {item_display}\n"

            content += "\n"

            content += f"[bold yellow]Exits:[/bold yellow]\n"
            for direction, destination_id in current_location["exits"].items():
                destination_name = locations[destination_id]["name"]
                content += f"   • {direction}: {destination_name}\n"

            console.print(
                Panel(
                    content,
                    title=f"[bold cyan]{current_location['name']}[/bold cyan]",
                    border_style="cyan",
                )
            )
        elif command == "quests":
            if len(player.active_quests) == 0:
                print_styled(
                    console, settings, "You have no active quests.", style="yellow"
                )
            else:
                console.clear()
                print_styled(console, settings, "=== Quest Log ===", style="bold cyan")

                quest_list = list(player.active_quests.keys())

                for index, quest_id in enumerate(quest_list, start=1):
                    quest_data = quests[quest_id]
                    status = player.active_quests[quest_id]["status"]

                    content = f"{index}. {quest_data['name']} ({status.capitalize()})"
                    print_styled(console, settings, content, style="cyan")

                console.print()
                user_choice = console.input("[bold cyan]> [/bold cyan]")

                if user_choice.strip() == "":
                    continue

                try:
                    quest_number = int(user_choice)

                    if 1 <= quest_number <= len(quest_list):
                        selected_quest_id = quest_list[quest_number - 1]
                        quest_data = quests[selected_quest_id]
                        status = player.active_quests[selected_quest_id]["status"]

                        content = f"[bold yellow]Status:[/bold yellow] {status.capitalize()}\n\n"
                        content += f"[bright_white]{quest_data['description']}[/bright_white]\n\n"

                        content += "[bold yellow]Objectives:[/bold yellow]\n"
                        for objective in quest_data["objectives"]:
                            if objective["completed"]:
                                marker = "✓"
                            else:
                                marker = "•"
                            content += f"  {marker} {objective['description']}\n"

                        content += "\n\n[bold yellow]Rewards:[/bold yellow]\n"
                        content += f"Gold: {quest_data['rewards']['gold']}"
                        for item in quest_data["rewards"]["items"]:
                            content += f"\n{item.replace("_", " ").title()}"

                        console.clear()
                        console.print(
                            Panel(
                                content,
                                title=f"[bold cyan]{quest_data['name']}[/bold cyan]",
                                border_style="cyan",
                            )
                        )
                    else:
                        print_styled(
                            console, settings, "Invalid quest number", style="red"
                        )
                except:
                    print_styled(
                        console, settings, "Please enter a valid number.", style="red"
                    )
        elif command == "save":
            save_game(player, locations, console, settings)
        elif command == "help":
            print_styled(
                console,
                settings,
                dedent(
                    """
            Available Commands:
                look - View detailed description of current location.
                go [direction] - Move in a direction (north, south, east, west).
                talk [npc name] - Talk to an NPC.
                take [item] - Pick up an item from the current location.
                inspect [item] - Examine an item in detail.
                inventory - View items you are carrying.
                use [item] - Use an item from your inventory.
                quests - View your active quests.
                save - Save your game progress.
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
