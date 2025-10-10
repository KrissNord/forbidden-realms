# Chapter 3: The Game Loop and Movement

## The Problem: A Static World

You can `look` around and see your location's description. That's great! But here's the issue:

**You can't go anywhere.**

Your game has multiple locations loaded in memory, but the player is stuck at the starting location. It's like loading a map but not being able to move on it.

What we need:
- A `go` command to move between locations
- Validation (can't walk through walls)
- Visual feedback when moving
- A way to see available exits

By the end of this chapter, you'll have a **fully explorable world**.

---

## Understanding Movement

Movement in a text game is simpler than it seems. Here's what really happens:

```
1. Player types: "go north"
2. Parse command → action="go", direction="north"
3. Check: Does current location have a north exit?
4. If yes:
   - Get destination ID from exits dictionary
   - Update current_location to point to new location
   - Display new location info
5. If no:
   - Show error message
```

**The key insight:** We're not "moving" the player through space. We're just **changing which dictionary** the `current_location` variable points to!

```python
# Before: current_location points to village_entrance
current_location = locations["village_entrance"]

# After "go north": current_location now points to town_square
current_location = locations["town_square"]
```

That's it. The "movement" is just updating a reference!

---

## Concept: Parsing Multi-Word Commands

You've seen this pattern before in Chapter 1, but let's understand it deeper.

**When a player types:**
```
go north
```

**Python sees it as one string:**
```python
command = "go north"
```

**We need to split it into parts:**

```python
parts = command.split()
# Result: ["go", "north"]

action = parts[0]      # "go"
direction = parts[1]   # "north"
```

**But what if the command is just one word?**

```python
command = "look"
parts = command.split()  # ["look"]
action = parts[0]         # "look"
direction = parts[1]      # ERROR! List index out of range
```

**Solution:** Check the length first:

```python
parts = command.split()

if len(parts) >= 2:
    action = parts[0]
    direction = parts[1]
    # Handle two-word commands (go, talk, take, etc.)
elif len(parts) == 1:
    action = parts[0]
    # Handle one-word commands (look, help, quit, etc.)
```

This pattern protects against index errors!

---

## Challenge 1: Implement the `go` Command

Time to make movement work!

### Step 1: Update Your Location Files

First, make sure your locations have exits that connect to each other.

**Update `data/locations/village_entrance.yaml`:**

```yaml
name: Village Entrance
short_description: A worn dirt path leads into the village.
detailed_description: >
  Two sturdy wooden posts mark the boundary of Runewild Village.
  Guard Tom stands watch here, greeting travelers.

exits:
  north: town_square    # Can go north to town square

npcs: []
items:
  - wooden_branch
```

**Update `data/locations/town_square.yaml`:**

```yaml
name: Town Square
short_description: The bustling heart of the village.
detailed_description: >
  The central plaza where merchants sell their wares and
  villagers gather to exchange news and gossip.

exits:
  south: village_entrance   # Can go back south

npcs: []
items:
  - gold_coin
```

Notice: **Village Entrance → north → Town Square** and **Town Square → south → Village Entrance**. They connect!

### Step 2: Parse Two-Word Commands

Modify your game loop to handle commands with multiple words.

**Current structure (from Chapter 1-2):**

```python
while True:
    command = console.input("[bold white]> [/bold white]")

    if command == "quit":
        break
    elif command == "look":
        # ... display location ...
```

**Problem:** This only handles exact matches. `command == "go north"` won't work because we need to check the action separately.

**New structure:**

```python
while True:
    command = console.input("[bold white]> [/bold white]")

    # TODO: Split command into parts
    parts = # ???

    # TODO: Check length and handle accordingly
    if len(parts) >= 2:
        # Two-word commands
        action = parts[0]

        if action == "go":
            # TODO: Handle movement

    elif len(parts) == 1:
        # One-word commands (same as before)
        action = parts[0]

        if action == "quit":
            break
        elif action == "look":
            # ... your look code ...
```

### Step 3: Implement Movement Logic

**Requirements:**
1. Get the direction from `parts[1]`
2. Check if that direction exists in `current_location["exits"]`
3. If yes:
   - Get the destination location ID
   - Update `current_location` to the new location
   - Display the new location's info
4. If no:
   - Show error message

**Skeleton:**

```python
if action == "go":
    # TODO: Get direction from command
    direction = # ???

    # TODO: Check if direction exists in exits
    if direction in current_location["exits"]:

        # TODO: Get destination location ID
        # Hint: current_location["exits"][direction] gives you the location_id
        new_location_id = # ???

        # TODO: Update current_location
        # Hint: current_location = locations[new_location_id]


        # TODO: Clear screen for clean look
        # Hint: console.clear()


        # TODO: Display new location name


        # TODO: Display new location short description


    else:
        # TODO: Show error - can't go that way
        # Hint: console.print(f"You can't go {direction} from here.", style="red")

```

### Guiding Questions

**Q1: How do I check if a key exists in a dictionary?**

<details>
<summary>Hint</summary>

Use the `in` operator:

```python
if "north" in current_location["exits"]:
    # North exit exists!
```

Or check all keys:

```python
available_exits = current_location["exits"].keys()
if direction in available_exits:
    # Exit exists
```
</details>

**Q2: How do I update current_location to point to a new location?**

<details>
<summary>Hint</summary>

```python
# Get the ID of the destination
destination_id = current_location["exits"]["north"]  # e.g., "town_square"

# Update current_location to point to that location's data
current_location = locations[destination_id]

# Now current_location is the town square dictionary
```
</details>

**Q3: How do I clear the screen?**

<details>
<summary>Hint</summary>

Rich console has a built-in method:

```python
console.clear()
```

This gives a fresh screen, making it easier to read the new location.
</details>

---

## Challenge 2: Better Entry Messages

Right now, when you move, you just see the location name and description. Let's make it prettier!

### Concept: Rich Panels for Movement

Instead of just printing text, let's use a panel to show the new location:

```python
from rich.panel import Panel

# When entering a new location
entry_content = f"[bright_white]{current_location['short_description']}[/bright_white]\n\n"
entry_content += f"[bold yellow]Exits:[/bold yellow] {', '.join(current_location['exits'].keys())}"

console.print(Panel(
    entry_content,
    title=f"[bold cyan]{current_location['name']}[/bold cyan]",
    border_style="cyan"
))
```

**Breaking it down:**

1. **`f"..."`** - f-string for embedding variables
2. **`current_location['short_description']`** - Get the short description
3. **`', '.join(...)`** - Join list of exits with commas ("north, south, east")
4. **Panel** - Wrap it in a nice bordered box

### Your Task: Enhanced Movement Display

When the player moves to a new location, display:
- Short description
- List of available exits (so they know where they can go)
- List of NPCs (if any)

**Skeleton:**

```python
if action == "go":
    direction = parts[1]

    if direction in current_location["exits"]:
        new_location_id = current_location["exits"][direction]
        current_location = locations[new_location_id]

        console.clear()

        # TODO: Build entry content string
        entry_content = # Start with short description


        # TODO: Add NPCs if any exist
        # Hint: if current_location["npcs"]:


        # TODO: Add exits
        # Hint: exit_directions = ", ".join(current_location["exits"].keys())


        # TODO: Display in panel
        # console.print(Panel(...))

```

---

## Challenge 3: Showing Available Exits

Players shouldn't have to `look` every time to see where they can go. Let's make exits visible in the `look` command and the movement panel.

### Concept: Formatting Exit Information

**Simple version:**
```python
exits = current_location["exits"]
exit_list = ", ".join(exits.keys())  # "north, south, east"
print(f"Exits: {exit_list}")
```

**Fancy version (with destinations):**
```python
exits = current_location["exits"]
exit_info = []

for direction, destination_id in exits.items():
    destination_name = locations[destination_id]["name"]
    exit_info.append(f"{direction}: {destination_name}")

# Result: "north: Town Square, south: Old Mill"
print(" | ".join(exit_info))
```

### Your Task: Update `look` Command

Modify your `look` command to show exits with their destinations.

**Example output:**
```
=== Village Entrance ===

Two sturdy wooden posts mark the boundary...

Exits:
  • north: Town Square
  • east: Old Mill
```

**Skeleton:**

```python
elif command == "look":
    # ... your existing look code ...

    # TODO: Add exits section
    content += "\n[bold yellow]Exits:[/bold yellow]\n"

    # TODO: Loop through exits
    for direction, destination_id in current_location["exits"].items():
        # TODO: Get destination name
        # Hint: locations[destination_id]["name"]


        # TODO: Add to content
        # content += f"   • {direction}: {destination_name}\n"

```

---

## Understanding the Game Loop Pattern

Your game loop now follows a classic pattern:

```python
while True:
    # 1. Get input
    command = console.input("> ")

    # 2. Parse input
    parts = command.split()

    # 3. Validate and dispatch
    if len(parts) >= 2:
        action = parts[0]
        if action == "go":
            # Handle movement
        elif action == "take":
            # Handle taking (future chapter)
    elif len(parts) == 1:
        action = parts[0]
        if action == "look":
            # Handle looking
        elif action == "quit":
            break

    # 4. Loop repeats
```

**This is the foundation of ALL interactive programs:**
- Input → Parse → Process → Output → Repeat

You'll see this pattern in web servers, game engines, chat bots, and more!

---

## Common Mistakes

### Mistake 1: Forgetting to update current_location

```python
# WRONG - gets the ID but doesn't update current_location
new_location_id = current_location["exits"]["north"]
# Still at old location!

# RIGHT - actually update the reference
current_location = locations[new_location_id]
```

### Mistake 2: Checking direction against wrong thing

```python
# WRONG - checking if direction is in the list of NPCs
if direction in current_location["npcs"]:

# RIGHT - check if direction is in exits
if direction in current_location["exits"]:
```

### Mistake 3: Not handling case sensitivity

```python
# Player types: "go North" (capital N)
# Your code checks: "North" in exits
# YAML has: "north" (lowercase)
# Result: "You can't go North from here" (even though north exists!)

# FIX - convert to lowercase
direction = parts[1].lower()
```

### Mistake 4: Exits point to non-existent locations

```yaml
# In village_entrance.yaml
exits:
  north: town_sqare  # TYPO! Should be "town_square"
```

**Result:** `KeyError: 'town_sqare'` when you try to move north.

**Prevention:** We'll build a validator in Chapter 4!

---

## Extension Ideas

### Extension 1: Cardinal Directions Shortcuts

Allow players to type just `n`, `s`, `e`, `w` instead of full direction names:

```python
# Direction aliases
direction_aliases = {
    "n": "north",
    "s": "south",
    "e": "east",
    "w": "west"
}

# In go command
direction = parts[1].lower()
if direction in direction_aliases:
    direction = direction_aliases[direction]
```

### Extension 2: Movement History

Track where the player has been:

```python
# At top of file
movement_history = []

# In go command, after moving
movement_history.append(new_location_id)

# New command to go back
elif action == "back":
    if len(movement_history) > 1:
        # Remove current location
        movement_history.pop()
        # Go to previous
        previous = movement_history[-1]
        current_location = locations[previous]
```

### Extension 3: Auto-Look After Movement

Automatically show the detailed description when entering a new location:

```python
# After moving
current_location = locations[new_location_id]

# Show entry panel (short description + exits)
# ... your panel code ...

# Then automatically "look"
# ... your look code here ...
```

---

## Testing Your Implementation

**Test Plan:**

1. **Start at Village Entrance**
   - Type `look` - should see detailed description
   - Should see exits listed

2. **Move to Town Square**
   - Type `go north`
   - Should clear screen
   - Should show Town Square panel
   - Should list exits (including south back to entrance)

3. **Return to Village Entrance**
   - Type `go south`
   - Should be back at entrance

4. **Try invalid direction**
   - Type `go east` (if no east exit)
   - Should show error message
   - Should stay at current location

5. **Try invalid command format**
   - Type just `go` (no direction)
   - Should handle gracefully (not crash)

---

## Debugging Corner

### Error: `KeyError: 'town_square'`

**Cause:** Trying to access a location that doesn't exist in the `locations` dictionary.

**Common reasons:**
- Typo in exit destination
- Location file not loaded
- File name doesn't match location ID

**Debug:**
```python
# Print all loaded location IDs
print("Loaded locations:", locations.keys())

# Check what the exit points to
print("North exit points to:", current_location["exits"]["north"])
```

### Error: `IndexError: list index out of range`

**Cause:** Trying to access `parts[1]` when player only typed one word.

**Example:**
```python
command = "go"   # Player forgot direction
parts = ["go"]   # Only one element
direction = parts[1]  # ERROR! No index 1
```

**Fix:** Check length first:
```python
if len(parts) >= 2:
    # Safe to access parts[1]
else:
    console.print("Go where?", style="red")
```

### Bug: Can move but see old location

**Cause:** Updated `current_location` but didn't display the new location info.

**Fix:** After updating `current_location`, make sure you display it:
```python
current_location = locations[new_location_id]
# Display new location here!
```

### Bug: Exits show IDs instead of names

**Output:** "Exits: town_square, old_mill"

**Wanted:** "Exits: Town Square, Old Mill"

**Fix:** Look up the location name:
```python
destination_name = locations[destination_id]["name"]
```

---

## What You've Learned

✅ **Command parsing** - Splitting multi-word input

✅ **List indexing** - Safely accessing elements by position

✅ **Dictionary navigation** - Following references through nested data

✅ **State management** - Updating what location the player is in

✅ **Input validation** - Checking if exits exist before using them

✅ **Screen management** - Clearing for better UX

✅ **The game loop pattern** - Input → Parse → Process → Output → Repeat

---

## Looking Ahead

In Chapter 4, you'll build **validators** - code that checks your data files for errors:

- Do all exits point to real locations?
- Are there any unreachable locations?
- Do NPCs referenced in locations actually exist?

Validators catch bugs before players find them!

In Chapter 5, you'll implement **save/load** so players can quit and resume later.

---

## Chapter 3 Checklist

Before moving on, make sure you can:

- [ ] Parse commands with multiple words
- [ ] Check the length of a list before accessing indexes
- [ ] Access nested dictionary values
- [ ] Update which dictionary a variable references
- [ ] Clear the console screen
- [ ] Display location info in a panel
- [ ] Loop through dictionary items (key-value pairs)
- [ ] Handle errors gracefully (invalid directions)

**All checked?** You now have an explorable world! 🗺️

---

## Final Thoughts

You just implemented **movement** - the most fundamental mechanic in exploration games. Think about it:

- Zelda: move between screens
- Skyrim: move through 3D space
- Your game: move between locations

**It's the same concept**, just different representations:
- 3D games track X, Y, Z coordinates
- 2D games track grid positions
- Your game tracks location IDs

The logic is identical: **check if movement is valid → update position → display new state**.

You're learning real game programming, not toy examples!

**Next:** In Chapter 4, we make your game robust with validators that catch content errors.

---

*"A journey of a thousand locations begins with a single `go north`."* - Wise Developer Saying
