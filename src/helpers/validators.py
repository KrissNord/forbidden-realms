from .display import print_styled


def validate_exits(locations, console, settings):
    has_errors = False

    for location_id, location_data in locations.items():
        exits = location_data["exits"]
        for direction, destination in exits.items():
            if destination in locations:
                pass
            else:
                print_styled(
                    console,
                    settings,
                    f"ERROR: Location '{location_id}' has exit '{direction}' pointing to missing location '{destination}'",
                    style="red",
                )
                has_errors = True

    return not has_errors


def validate_npcs(locations, npcs, console, settings):
    has_errors = False

    for location_id, location_data in locations.items():
        npc = location_data["npcs"]
        if npc is not None:
            for item in npc:
                if item in npcs:
                    pass
                else:
                    print_styled(
                        console,
                        settings,
                        f"ERROR: Location '{location_id}' has missing npc '{item}'",
                        style="red",
                    )
                    has_errors = True

    return not has_errors


def validate_graph_connectivity(locations, console, settings):
    if not locations:
        return True

    starting_location = "village_entrance"
    visited = set()
    to_visit = [starting_location]

    while to_visit:
        current_location_id = to_visit.pop(0)
        visited.add(current_location_id)

        current_location_data = locations[current_location_id]
        exits = current_location_data["exits"]
        for direction, destination in exits.items():
            if destination not in visited and destination not in to_visit:
                to_visit.append(destination)
            else:
                pass

    all_locations = set(locations.keys())
    has_errors = False

    for location in all_locations:
        if location in visited:
            pass
        else:
            has_errors = True
            print_styled(
                console,
                settings,
                f"ERROR: Location '{location}' is unreachable.",
                style="red",
            )

    return not has_errors


def validate_items(locations, items, console, settings):
    has_errors = False

    for location_id, location_data in locations.items():
        location_items = location_data.get("items", [])
        if location_items:
            for item_id in location_items:
                if item_id not in items:
                    print_styled(
                        console,
                        settings,
                        f"ERROR: Location '{location_id}' references missing item '{item_id}'",
                        style="red",
                    )
                    has_errors = True

    return not has_errors
