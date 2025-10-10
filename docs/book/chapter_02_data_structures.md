# Chapter 2: Data Structures - Representing Your World

## The Problem: Hardcoded Content

In Chapter 1, you created a game loop that responds to commands. But here's a question: **Where does your game world actually exist?**

Right now, it doesn't. To add a location, you'd have to write code like this:

```python
# DON'T DO THIS
if player_location == "village_entrance":
    print("A worn dirt path leads into the village.")
    print("You can go: north, east")
elif player_location == "town_square":
    print("The town square is bustling with life.")
    print("You can go: south, west")
# ... and 50 more locations
```

**Problems with this approach:**

❌ **Code and content mixed** - Want to change a description? Edit code.

❌ **No collaboration** - Writers can't add content without knowing Python.

❌ **Error prone** - One typo breaks the game.

❌ **Hard to maintain** - Imagine 100 locations in if/elif chains.

❌ **Can't reload** - Must restart game to see content changes.

**The solution:** Separate **data** (content) from **code** (logic).

---

## Enter YAML: Your Game's Database

**YAML** (YAML Ain't Markup Language) is a human-readable data format. Think of it as a simple database for your game.

**Why YAML instead of JSON or XML?**

✅ **Readable** - Looks like a simple outline, not code

✅ **No clutter** - No curly braces, brackets, or closing tags

✅ **Multiline strings** - Perfect for descriptions

✅ **Comments** - Document your content inline

### Example: Location in YAML

```yaml
name: Village Entrance
short_description: A worn dirt path leads into the village.
detailed_description: >
  Two sturdy wooden posts mark the boundary of Runewild Village.
  A dirt path, rutted from wagon wheels, winds between them.
  Guard Tom stands watch, eyes scanning each newcomer.
exits:
  north: town_square
  east: old_mill
npcs:
  - guard_tom
items:
  - small_health_potion
```

**Clean, right?** A writer could edit this file without knowing any Python.

---

## Python Data Structures: Dictionaries and Lists

When Python loads a YAML file, it converts it to **dictionaries** and **lists**.

### Concept: Dictionaries

A **dictionary** is a collection of key-value pairs:

```python
location = {
    "name": "Village Entrance",
    "description": "A worn dirt path leads into the village.",
    "exits": {"north": "town_square", "east": "old_mill"}
}
```

**Accessing values:**

```python
print(location["name"])              # "Village Entrance"
print(location["exits"]["north"])    # "town_square"
```

**Key points:**
- Use **square brackets** with the key name
- Keys are strings (in quotes)
- Values can be strings, numbers, lists, or other dictionaries
- **Nested dictionaries** are dictionaries inside dictionaries

### Concept: Lists

A **list** is an ordered collection:

```python
items = ["health_potion", "wooden_branch", "gold_coin"]
npcs = ["guard_tom", "merchant_sara"]
```

**Accessing elements:**

```python
print(items[0])      # "health_potion" (first item)
print(items[1])      # "wooden_branch" (second item)
print(len(items))    # 3 (number of items)
```

**Checking if something is in a list:**

```python
if "guard_tom" in npcs:
    print("Guard Tom is here!")
```

**Key points:**
- Use **square brackets** with an index (number)
- Indexes start at **0**, not 1
- Use `len()` to get the number of elements
- Use `in` to check membership

---

## Challenge 1: Your First Location

Let's create a location file and load it into your game.

### Step 1: Create the Directory Structure

```bash
mkdir -p data/locations
```

This creates nested directories: `data/` and inside it, `locations/`.

### Step 2: Create Your First Location File

Create `data/locations/village_entrance.yaml` and add this content:

```yaml
name: Village Entrance
short_description: A worn dirt path leads into the village.
detailed_description: >
  Two sturdy wooden posts mark the boundary of Runewild Village, their surfaces
  weathered by countless seasons. A dirt path, rutted from wagon wheels and worn
  smooth by travelers' boots, winds between them and into the heart of the settlement.

exits:
  north: town_square

npcs: []

items:
  - wooden_branch
```

**Note the syntax:**
- `name:` is a string value
- `exits:` is a dictionary (key-value pairs indented below)
- `npcs:` is an empty list (`[]`)
- `items:` is a list with one element

**The `>` symbol:** Means "fold the following lines into one paragraph." Makes long descriptions readable in the file.

---

## Challenge 2: Loading YAML in Python

Now let's load this file into your game.

### Concept: Loading YAML Files

```python
import yaml

# Open the file
with open("data/locations/village_entrance.yaml", "r") as file:
    # Parse YAML into Python dictionary
    location_data = yaml.safe_load(file)

# Now location_data is a dictionary you can use
print(location_data["name"])
```

**Breaking it down:**

1. **`import yaml`** - Load the PyYAML library
2. **`with open(...) as file:`** - Opens the file (and auto-closes when done)
3. **`yaml.safe_load(file)`** - Converts YAML text to Python dictionary
4. **`location_data`** - Now a regular Python dict you can access

### Your Task: Load and Display

Modify your `main.py` to load the location and display it.

**Requirements:**
1. Import the yaml module
2. Load `data/locations/village_entrance.yaml`
3. After your title screen, display:
   - Location name (in bold cyan)
   - Short description
4. Then start the game loop

**Skeleton Code:**

```python
import yaml
from rich.console import Console
from rich.panel import Panel

console = Console()

# ... your title screen code from Chapter 1 ...

# TODO: Load the location file
# Hint: with open("data/locations/village_entrance.yaml", "r") as file:
#           location_data = yaml.safe_load(file)


# TODO: Display the location name
# Hint: console.print(location_data["name"], style="bold cyan")


# TODO: Display the short description


# Game loop from Chapter 1
while True:
    command = console.input("[bold white]> [/bold white]")

    if command == "quit":
        break
    elif command == "help":
        console.print("Commands: look, quit, help", style="blue")
    else:
        console.print(f"Unknown command: {command}", style="red")
```

**Test it:**

```bash
python main.py
```

You should see the title, then "Village Entrance" and its description, then the prompt.

---

## Challenge 3: The `look` Command

Let's make the `look` command actually show the detailed description.

### Concept: Accessing Nested Data

Your location dictionary has this structure:

```python
location_data = {
    "name": "Village Entrance",
    "detailed_description": "Two sturdy wooden posts...",
    "exits": {"north": "town_square"},
    "items": ["wooden_branch"]
}
```

**To access:**

```python
location_data["name"]                    # "Village Entrance"
location_data["detailed_description"]    # Long description
location_data["exits"]["north"]          # "town_square"
location_data["items"][0]                # "wooden_branch"
```

### Your Task: Implement `look`

When the player types `look`, display:
- The location name (as a panel title)
- The detailed description
- Exits (list of directions)
- Items (if any)
- NPCs (if any)

**Skeleton:**

```python
# In your game loop, add:

elif command == "look":
    # TODO: Create content string
    content = ""

    # TODO: Add detailed description
    # Hint: content += location_data["detailed_description"]


    # TODO: Add newlines for spacing
    # content += "\n\n"


    # TODO: Add exits section
    # Hint: exits = location_data["exits"]
    # Loop through exits.keys() to show available directions


    # TODO: Add items section (if any items exist)
    # Hint: if location_data["items"]:
    #           for item in location_data["items"]:


    # TODO: Display in a panel
    # Hint: console.print(Panel(content,
    #                          title=location_data["name"],
    #                          border_style="cyan"))
```

### Guiding Questions

**Q1: How do I loop through dictionary keys?**

<details>
<summary>Hint</summary>

```python
exits = location_data["exits"]
for direction in exits.keys():
    print(direction)  # "north", "east", etc.
```

Or get both key and value:

```python
for direction, destination in exits.items():
    print(f"{direction}: {destination}")
```
</details>

**Q2: How do I check if a list is empty before displaying it?**

<details>
<summary>Hint</summary>

```python
if location_data["items"]:  # True if list has elements
    # Display items
```

Or check length:

```python
if len(location_data["items"]) > 0:
    # Display items
```
</details>

**Q3: How do I format item names nicely?**

<details>
<summary>Hint</summary>

YAML has `wooden_branch`, but you want to display "Wooden Branch":

```python
item = "wooden_branch"
formatted = item.replace("_", " ").title()  # "Wooden Branch"
```
</details>

---

## Challenge 4: Loading Multiple Locations

One location is boring. Let's load **all** location files automatically.

### Concept: Listing Files in a Directory

```python
import os

files = os.listdir("data/locations")
# Returns: ["village_entrance.yaml", "town_square.yaml", ...]
```

Then filter for `.yaml` files:

```python
for filename in files:
    if filename.endswith(".yaml"):
        # This is a YAML file
```

### Concept: Building a Dictionary of Locations

Instead of one location, let's create a dictionary of all locations:

```python
locations = {
    "village_entrance": { name, description, exits... },
    "town_square": { name, description, exits... },
    ...
}
```

**The pattern:**

```python
locations = {}

for filename in os.listdir("data/locations"):
    if filename.endswith(".yaml"):
        # Get ID from filename
        location_id = filename.replace(".yaml", "")  # "village_entrance"

        # Load the file
        with open(f"data/locations/{filename}", "r") as file:
            location_data = yaml.safe_load(file)

        # Add to dictionary
        locations[location_id] = location_data
```

Now `locations["village_entrance"]` gives you that location's data!

### Your Task: Load All Locations

Before we can use this, you need more location files. Let's create a second location.

**Step 1:** Create `data/locations/town_square.yaml`:

```yaml
name: Town Square
short_description: The town square is bustling with life.
detailed_description: >
  The heart of Runewild Village, where stone pathways converge around
  a central fountain. Merchants call out their wares from colorful stalls,
  children play near the fountain, and the smell of fresh bread drifts
  from the baker's shop.

exits:
  south: village_entrance

npcs: []

items:
  - gold_coin
```

**Step 2:** Modify `main.py` to load all locations into a dictionary.

**Skeleton:**

```python
import os
import yaml
from rich.console import Console
from rich.panel import Panel

console = Console()

# ... title screen code ...

# TODO: Create empty locations dictionary


# TODO: Loop through files in data/locations/


# TODO: For each .yaml file:
#   - Get location_id from filename
#   - Load the file
#   - Add to locations dictionary


# TODO: Set starting location
# current_location = locations["village_entrance"]


# Display starting location name and description
# TODO: Use current_location instead of location_data


# Game loop
while True:
    command = console.input("[bold white]> [/bold white]")

    if command == "quit":
        break
    elif command == "look":
        # TODO: Update to use current_location
        pass
    elif command == "help":
        console.print("Commands: look, quit, help", style="blue")
```

**Test:**

```bash
python main.py
```

You should still start at Village Entrance, but now the game has loaded Town Square too (you just can't move there yet).

---

## Understanding the Data Flow

Let's trace how data moves through your program:

```
1. Files on disk:
   village_entrance.yaml
   town_square.yaml

2. Load into Python:
   locations = {
       "village_entrance": {...},
       "town_square": {...}
   }

3. Track current location:
   current_location = locations["village_entrance"]

4. Display location data:
   current_location["name"]
   current_location["description"]
```

**Key insight:** `current_location` is a **reference** to one of the dictionaries in `locations`. When you change which location the player is in, you just update that reference!

---

## What You've Learned

✅ **YAML basics** - Human-readable data format

✅ **Dictionaries** - Key-value pairs, accessing nested data

✅ **Lists** - Ordered collections, iteration, membership checking

✅ **File I/O** - Loading files with `open()`

✅ **Data organization** - Separating content from code

✅ **Directory operations** - Listing files with `os.listdir()`

✅ **String formatting** - Making IDs into readable names

---

## Common Mistakes

### Mistake 1: Forgetting to import yaml

```python
# ERROR
location_data = yaml.safe_load(file)
# NameError: name 'yaml' is not defined

# FIX
import yaml  # Add at top of file
```

### Mistake 2: Wrong path to file

```python
# ERROR - missing data/ prefix
with open("locations/village_entrance.yaml", "r") as file:

# FIX
with open("data/locations/village_entrance.yaml", "r") as file:
```

### Mistake 3: Trying to access dict before loading

```python
# ERROR - location_data doesn't exist yet
print(location_data["name"])
with open(...) as file:
    location_data = yaml.safe_load(file)

# FIX - load first, then access
with open(...) as file:
    location_data = yaml.safe_load(file)
print(location_data["name"])
```

### Mistake 4: Confusing list index with dict key

```python
items = ["potion", "sword"]

# ERROR - lists use numeric indexes
items["potion"]  # TypeError

# FIX
items[0]  # "potion"

# For membership checking, use 'in'
if "potion" in items:
    print("Found it!")
```

---

## Extension Ideas

### Extension 1: Location Inspector

Create a command that shows the raw data structure:

```python
elif command == "debug":
    import json
    print(json.dumps(current_location, indent=2))
```

This helps you see exactly what data you're working with.

### Extension 2: Create More Locations

Add 2-3 more locations:
- Old Mill
- Market Street
- Tavern

Connect them with exits to build a small world.

### Extension 3: Location Validation

Check if all exits point to locations that exist:

```python
for location_id, location_data in locations.items():
    for direction, destination in location_data["exits"].items():
        if destination not in locations:
            print(f"ERROR: {location_id} has exit to non-existent {destination}")
```

---

## Debugging Corner

### Error: `yaml.scanner.ScannerError`

**Cause:** Syntax error in YAML file (wrong indentation, missing colon, etc.)

**Example:**
```yaml
name: Village
exits
  north: town  # Missing colon after 'exits'
```

**Fix:** Check YAML syntax. Common issues:
- Forgot colon after key
- Inconsistent indentation (mix of tabs and spaces)
- Missing quotes around special characters

### Error: `KeyError: 'name'`

**Cause:** Trying to access a key that doesn't exist in the dictionary.

**Fix:** Check your YAML file has that field. Or use `.get()`:

```python
# ERROR if key missing
location_data["name"]

# Returns None if key missing (no error)
location_data.get("name")

# Returns default if key missing
location_data.get("name", "Unknown Location")
```

### Error: `FileNotFoundError`

**Cause:** File path is wrong.

**Debug steps:**
```python
import os
print(os.getcwd())  # Check current directory
print(os.listdir("data"))  # Check what's in data/
```

---

## Looking Ahead

In Chapter 3, you'll implement the `go` command so players can actually move between locations. You'll learn about:

- Parsing multi-word commands
- Updating game state
- Clearing the screen
- Error handling

By the end of Chapter 3, you'll have a world players can explore!

---

## Chapter 2 Checklist

Before moving on, make sure you can:

- [ ] Explain the difference between dictionaries and lists
- [ ] Load a YAML file into Python
- [ ] Access nested dictionary values
- [ ] Loop through dictionary keys
- [ ] Check if an element is in a list
- [ ] List files in a directory
- [ ] Build a dictionary from multiple files
- [ ] Display location data in a formatted panel

**All checked?** Time for Chapter 3! 🗺️

---

## Final Thoughts

You've just separated your game's **content** (YAML files) from its **logic** (Python code). This is a fundamental principle of game development.

**Why this matters:**

- **Writers** can add content without touching code
- **Designers** can tweak balance in data files
- **Translators** can create localized versions
- **Modders** can create custom content
- **You** can test changes without recompiling

Professional games work exactly like this - data-driven design is how AAA studios manage thousands of items, quests, and characters.

**Next:** In Chapter 3, we'll connect these locations and let players move through your world.

---

*"Data is the fuel, code is the engine, and game design is the driver."* - Ancient Game Developer Wisdom
