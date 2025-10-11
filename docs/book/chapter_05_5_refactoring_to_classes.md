# Chapter 5.5: Refactoring to Classes - Better Code Organization

## The Problem: Scattered State

You've built an impressive game through Chapters 1-5! But let's look at what you're tracking:

```python
# At the top of main.py
current_location = "village_entrance"
inventory = []

# Maybe also:
current_health = 100
current_gold = 0
```

**This works, but it has problems:**

❌ **Scattered data** - Player info spread across multiple variables

❌ **Hard to pass around** - Every function needs all these variables as parameters

❌ **Difficult to extend** - Adding player stats means more global variables

❌ **No encapsulation** - Any code can modify player data

**The solution:** Organize related data into a **class**.

---

## What You'll Learn

By the end of this chapter:
- ✅ Understand what classes and objects are
- ✅ Create a Player class to organize game state
- ✅ Refactor existing code to use the class
- ✅ Know when to use classes vs simple variables
- ✅ Have cleaner, more maintainable code

**Important:** This is a **refactoring chapter** - your game will do the same things, just with better organization.

---

## Concept: What Are Classes?

A **class** is a blueprint for creating objects that group related data and functions together.

### Real-World Analogy

Think of a **character sheet** in a tabletop RPG:

```
┌─────────────────────────┐
│  CHARACTER SHEET        │
├─────────────────────────┤
│ Name: Alice             │
│ Location: Village       │
│ Health: 100/100         │
│ Gold: 50                │
│                         │
│ Inventory:              │
│  - Health Potion        │
│  - Wooden Branch        │
│                         │
│ [Rest] [Attack] [Flee]  │
└─────────────────────────┘
```

A **class** is like the blank character sheet template.

An **object** (or **instance**) is a filled-in sheet for a specific character.

### Classes in Python

**Defining a class (the blueprint):**

```python
class Player:
    def __init__(self, starting_location):
        # __init__ runs when you create a new player
        self.current_location = starting_location
        self.inventory = []
        self.health = 100
        self.gold = 0
```

**Creating an object (filling in the sheet):**

```python
# Create a new player
player = Player("village_entrance")

# Access data with dot notation
print(player.current_location)  # "village_entrance"
print(player.inventory)          # []
print(player.health)             # 100

# Modify data
player.gold = 50
player.inventory.append("wooden_branch")
```

**Key concepts:**
- **`class Player:`** - Defines the blueprint
- **`__init__`** - Special method that runs when creating an object (constructor)
- **`self`** - Refers to the specific object (like "this sheet")
- **`self.current_location`** - Data that belongs to this player
- **`player = Player(...)`** - Creates a new object from the class

---

## Why Classes Make Code Better

### Before: Scattered Variables

```python
# main.py
current_location = "village_entrance"
inventory = []
health = 100
gold = 0

def take_item(item, inventory, locations, current_location):
    # Need to pass everything!
    if item in locations[current_location]["items"]:
        locations[current_location]["items"].remove(item)
        inventory.append(item)

def save_game(current_location, inventory, health, gold, locations):
    # So many parameters!
    save_data = {
        "current_location": current_location,
        "inventory": inventory,
        "health": health,
        "gold": gold,
        # ...
    }
```

### After: Organized Class

```python
# src/character/player.py
class Player:
    def __init__(self, starting_location):
        self.current_location = starting_location
        self.inventory = []
        self.health = 100
        self.gold = 0

# main.py
player = Player("village_entrance")

def take_item(item, player, locations):
    # Pass one player object instead of many variables!
    if item in locations[player.current_location]["items"]:
        locations[player.current_location]["items"].remove(item)
        player.inventory.append(item)

def save_game(player, locations):
    # Much cleaner!
    save_data = {
        "current_location": player.current_location,
        "inventory": player.inventory,
        "health": player.health,
        "gold": player.gold,
        # ...
    }
```

**Benefits:**
- ✅ Related data grouped together
- ✅ Fewer function parameters
- ✅ Clear ownership (this is player data)
- ✅ Easy to extend (add new player attributes)

---

## Challenge 1: Create the Player Class

Let's create a simple Player class to organize our game state.

### Step 1: Create the File

```bash
# Create directory if it doesn't exist
mkdir -p src/character

# Create the file
# On macOS/Linux:
touch src/character/player.py

# On Windows:
type nul > src\character\player.py
```

### Step 2: Implement the Class

**Requirements:**
1. Class named `Player`
2. `__init__` method that takes `starting_location`
3. Attributes: `current_location`, `inventory`, `health`, `gold`
4. Set default values for health (100) and gold (0)

**Skeleton:**

```python
# src/character/player.py

class Player:
    """
    Represents the player character in the game.

    Attributes:
        current_location: ID of the current location (e.g., "village_entrance")
        inventory: List of item IDs the player is carrying
        health: Player's current health points
        gold: Amount of gold the player has
    """

    def __init__(self, starting_location):
        """
        Create a new player.

        Args:
            starting_location: ID of the location where player starts
        """
        # TODO: Set current_location to starting_location
        # Hint: self.current_location = starting_location


        # TODO: Initialize empty inventory
        # Hint: self.inventory = []


        # TODO: Set starting health to 100
        # Hint: self.health = 100


        # TODO: Set starting gold to 0
        # Hint: self.gold = 0
```

### Step 3: Test Your Class

Before integrating into the game, let's test it works:

```python
# test_player.py (create this temporarily)
from src.character.player import Player

# Create a player
player = Player("village_entrance")

# Test attributes
print(f"Location: {player.current_location}")  # Should be "village_entrance"
print(f"Inventory: {player.inventory}")         # Should be []
print(f"Health: {player.health}")               # Should be 100
print(f"Gold: {player.gold}")                   # Should be 0

# Test modifications
player.inventory.append("wooden_branch")
player.gold = 25
print(f"Inventory after: {player.inventory}")   # ["wooden_branch"]
print(f"Gold after: {player.gold}")             # 25
```

**Run the test:**

```bash
python test_player.py
```

If everything prints correctly, your class works! You can delete `test_player.py` now.

---

## Challenge 2: Refactor main.py

Now let's update your game to use the Player class.

### Step 1: Import the Player Class

At the top of `main.py`, add:

```python
from src.character.player import Player
```

### Step 2: Replace Variables with Player Object

**Find this pattern in your code:**

```python
# OLD
current_location = "village_entrance"
inventory = []
```

**Replace with:**

```python
# NEW
player = Player("village_entrance")
```

### Step 3: Update References Throughout

Now you need to find every place that uses the old variables and update them.

**Pattern 1: Reading current_location**

```python
# OLD
if direction in current_location["exits"]:

# NEW
if direction in locations[player.current_location]["exits"]:
```

**Wait, what changed?**
- `current_location` was a dictionary (the actual location data)
- `player.current_location` is a string (the location ID)
- So we need: `locations[player.current_location]` to get the dictionary

**Pattern 2: Updating current_location**

```python
# OLD
current_location = locations[new_location_id]

# NEW
player.current_location = new_location_id
```

**Pattern 3: Inventory operations**

```python
# OLD
inventory.append(item)
if item in inventory:

# NEW
player.inventory.append(item)
if item in player.inventory:
```

### Step 4: Update Game Loop Commands

Go through your game loop and update all commands:

**`go` command:**

```python
elif action == "go":
    if len(parts) < 2:
        console.print("Go where?", style="red")
    else:
        direction = parts[1].lower()

        # TODO: Get current location data from locations dict
        # Hint: current_loc_data = locations[player.current_location]


        # TODO: Check if direction exists in exits
        if direction in # ???:

            # TODO: Get destination ID
            new_location_id = # ???

            # TODO: Update player's location (store the ID, not the dict)
            player.current_location = # ???

            console.clear()

            # TODO: Get the new location data for display
            # Hint: new_loc_data = locations[player.current_location]


            # TODO: Display location info using new_loc_data
```

**`look` command:**

```python
elif action == "look":
    # TODO: Get current location data
    current_loc_data = locations[player.current_location]

    # TODO: Build and display content using current_loc_data
    content = f"{current_loc_data['detailed_description']}\n\n"
    # ... rest of look command
```

**`inventory` command:**

```python
elif action == "inventory":
    # TODO: Check if player has items
    if player.inventory:
        console.print("[bold cyan]Inventory:[/bold cyan]")
        for item in player.inventory:
            # Display items
    else:
        console.print("Your inventory is empty.", style="dim")
```

### Step 5: Update Save/Load Functions

In `src/helpers/save_load.py`:

**save_game function:**

```python
def save_game(player, locations, console, settings):
    """Save the current game state"""

    # ... directory creation ...

    # Build save data - now from player object
    save_data = {
        "version": "0.0.1",
        "current_location": player.current_location,  # Changed
        "inventory": player.inventory,                 # Changed
        "location_items": {
            loc_id: loc_data["items"]
            for loc_id, loc_data in locations.items()
        }
    }

    # ... rest of save function ...
```

**load_game function:**

```python
def load_game(player, locations, console, settings):
    """Load a saved game"""

    # ... file loading ...

    # Restore player state
    player.current_location = loaded_data["current_location"]  # Changed
    player.inventory = loaded_data["inventory"]                 # Changed

    # ... restore location items ...

    return loaded_data
```

**Update main.py to pass player:**

```python
# OLD
elif action == "save":
    save_game(current_location, inventory, locations, console, settings)

# NEW
elif action == "save":
    save_game(player, locations, console, settings)

# OLD
elif action == "load":
    result = load_game(current_location, inventory, locations, console, settings)

# NEW
elif action == "load":
    result = load_game(player, locations, console, settings)
```

---

## Challenge 3: Test the Refactored Game

**Critical:** After refactoring, test **everything** to make sure it still works!

### Test Checklist

1. **Start game**
   - ✅ Loads at village entrance
   - ✅ No errors on startup

2. **Movement**
   - ✅ `go north` works
   - ✅ `go south` back works
   - ✅ `go invalid` shows error

3. **Look command**
   - ✅ Shows current location correctly
   - ✅ Shows exits
   - ✅ Shows items

4. **Inventory**
   - ✅ `take item` adds to inventory
   - ✅ `inventory` shows items
   - ✅ Items display correctly

5. **Save/Load**
   - ✅ `save` creates save file
   - ✅ `quit` exits
   - ✅ Restart and `load` works
   - ✅ Location and inventory restored
   - ✅ **Items don't respawn** (critical!)

**If anything breaks:** Check the Debugging Corner at the end of this chapter.

---

## Understanding self

The `self` parameter confuses many beginners. Let's demystify it.

### What is self?

**`self` is how a method refers to the specific object it's working with.**

**Analogy:** Imagine you're in a classroom. The teacher says "Raise your hand." The word "your" is like `self` - it means "the hand belonging to you specifically."

### Example Without Classes

```python
# Without classes
player1_name = "Alice"
player1_health = 100

player2_name = "Bob"
player2_health = 80

def heal_player(name, health):
    health += 20
    print(f"{name} healed to {health}")

heal_player(player1_name, player1_health)  # Which player? Have to specify!
```

### Example With Classes

```python
# With classes
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100

    def heal(self):
        self.health += 20
        print(f"{self.name} healed to {self.health}")

player1 = Player("Alice")
player2 = Player("Bob")

player1.heal()  # Heals Alice - self is player1
player2.heal()  # Heals Bob - self is player2
```

**When you call `player1.heal()`:**
1. Python finds the `heal` method in the `Player` class
2. Automatically passes `player1` as the first argument (`self`)
3. Inside the method, `self` refers to `player1`

**Think of it this way:**
- `player1.heal()` really means `Player.heal(player1)`
- `self` is the object the method is called on

---

## Adding Methods to Your Player Class

Right now, your Player class just holds data. You can also add **methods** - functions that operate on that data.

### Example: Add a method to display player status

```python
class Player:
    def __init__(self, starting_location):
        self.current_location = starting_location
        self.inventory = []
        self.health = 100
        self.gold = 0

    def display_status(self):
        """Display player status in a formatted panel"""
        from rich.panel import Panel
        from rich.console import Console

        console = Console()

        content = f"[bold yellow]Health:[/bold yellow] {self.health}/100\n"
        content += f"[bold yellow]Gold:[/bold yellow] {self.gold}\n"
        content += f"[bold yellow]Items:[/bold yellow] {len(self.inventory)}"

        console.print(Panel(content, title="[bold cyan]Player Status[/bold cyan]", border_style="cyan"))
```

**Using it in your game:**

```python
elif action == "status":
    player.display_status()
```

**Why is this better?**
- The display logic lives with the Player class
- Any code with a player object can call `display_status()`
- If you change how status is displayed, change it in one place

---

## Common Mistakes

### Mistake 1: Forgetting self

```python
# WRONG
class Player:
    def __init__(self, starting_location):
        current_location = starting_location  # Missing self!
        inventory = []                         # Missing self!

# This creates local variables, not attributes!
```

**Fix:** Always use `self.` for attributes:

```python
# RIGHT
class Player:
    def __init__(self, starting_location):
        self.current_location = starting_location
        self.inventory = []
```

### Mistake 2: Passing self manually

```python
# WRONG
player = Player("village_entrance")
player.display_status(player)  # Don't pass self!

# RIGHT
player.display_status()  # Python passes self automatically
```

### Mistake 3: Confusing location ID with location data

```python
# WRONG
player.current_location = locations["village_entrance"]  # Stores the dict!

# RIGHT
player.current_location = "village_entrance"  # Stores the ID string

# To get the dict, use:
current_loc_data = locations[player.current_location]
```

This is the biggest refactoring mistake. Remember:
- **Before refactoring:** `current_location` was the dictionary
- **After refactoring:** `player.current_location` is the ID string

### Mistake 4: Not updating all references

After refactoring, if you miss updating a reference, you'll get errors:

```python
# OLD code you forgot to update
if direction in current_location["exits"]:  # NameError: current_location not defined

# Should be
if direction in locations[player.current_location]["exits"]:
```

**Tip:** Use your editor's Find & Replace to find all instances of:
- `current_location` → `player.current_location` (or `locations[player.current_location]`)
- `inventory` → `player.inventory`

---

## Extension Ideas

### Extension 1: Add Player Methods

Add helpful methods to the Player class:

```python
def add_gold(self, amount):
    """Add gold to player's purse"""
    self.gold += amount

def remove_gold(self, amount):
    """Remove gold (returns False if not enough)"""
    if self.gold >= amount:
        self.gold -= amount
        return True
    return False

def has_item(self, item_id):
    """Check if player has an item"""
    return item_id in self.inventory

def take_damage(self, amount):
    """Reduce health by amount"""
    self.health = max(0, self.health - amount)  # Don't go below 0

def heal(self, amount):
    """Restore health"""
    self.health = min(100, self.health + amount)  # Don't exceed 100
```

### Extension 2: Player Stats Display

Add a command to show detailed player stats:

```python
elif action == "stats":
    console.print(f"[bold cyan]Character Stats[/bold cyan]")
    console.print(f"Location: {locations[player.current_location]['name']}")
    console.print(f"Health: {player.health}/100")
    console.print(f"Gold: {player.gold}")
    console.print(f"Items: {len(player.inventory)}")
```

### Extension 3: Encapsulation (Advanced)

Add validation when setting values:

```python
class Player:
    def __init__(self, starting_location):
        self.current_location = starting_location
        self.inventory = []
        self._health = 100  # Underscore indicates "private"
        self._gold = 0

    @property
    def health(self):
        """Get current health"""
        return self._health

    @health.setter
    def health(self, value):
        """Set health with validation"""
        if value < 0:
            self._health = 0
        elif value > 100:
            self._health = 100
        else:
            self._health = value

    # Now: player.health = 150 automatically caps at 100
```

---

## Debugging Corner

### Error: `NameError: name 'current_location' is not defined`

**Cause:** You forgot to update a reference from the old variable to the player object.

**Fix:** Find all instances of `current_location` and update to `player.current_location` (or `locations[player.current_location]` if you need the data).

### Error: `TypeError: string indices must be integers`

**Cause:** You're treating a string like a dictionary.

**Problem:**
```python
player.current_location = "village_entrance"  # String
if direction in player.current_location["exits"]:  # Can't do ["exits"] on string!
```

**Fix:**
```python
current_loc_data = locations[player.current_location]
if direction in current_loc_data["exits"]:
```

### Error: `AttributeError: 'Player' object has no attribute 'inventory'`

**Cause:** You forgot to initialize the attribute in `__init__`.

**Fix:** Make sure your `__init__` sets all attributes:
```python
def __init__(self, starting_location):
    self.current_location = starting_location
    self.inventory = []  # Don't forget this!
    self.health = 100
    self.gold = 0
```

### Bug: Save/load doesn't work after refactoring

**Cause:** You updated main.py but forgot to update `save_load.py`.

**Fix:** Make sure both `save_game()` and `load_game()` accept a `player` parameter and use `player.current_location` and `player.inventory`.

### Bug: Items respawn after refactoring

**Cause:** You're checking the old `inventory` list somewhere.

**Fix:** Search your code for just `inventory` (not `player.inventory`) and update it.

---

## What You've Learned

✅ **Object-Oriented Programming** - Classes, objects, attributes, methods

✅ **Refactoring** - Improving code structure without changing behavior

✅ **Encapsulation** - Grouping related data together

✅ **The self parameter** - How methods reference their object

✅ **Code organization** - When to use classes vs simple variables

✅ **Migration strategy** - How to update existing working code

✅ **Testing** - Verifying behavior after refactoring

---

## When to Use Classes

**Use classes when:**
- ✅ You have related data that belongs together (player stats, location data)
- ✅ You're passing many variables together as parameters
- ✅ You need multiple instances (multiple players, enemies, items)
- ✅ You want to add behavior with methods

**Use simple variables when:**
- ✅ Single unrelated values (game_running = True)
- ✅ Temporary calculations (total_damage = base + bonus)
- ✅ Simple counters (turn_number = 1)

**In Forbidden Realms:**
- **Player** → Class (has location, inventory, stats, methods)
- **Locations** → Dictionary (loaded from YAML, mostly static)
- **Items** → Dictionary (loaded from YAML, mostly static)
- **Settings** → Dictionary (simple configuration)

Later, you might create classes for NPCs, Quests, Items (if they have complex behavior).

---

## Looking Ahead

**You're now ready for Milestone 1 and beyond!**

Your code is organized with a Player class, which means:
- ✅ Easy to add player stats (strength, intelligence, etc.)
- ✅ Easy to add player methods (attack, defend, cast_spell)
- ✅ Clean function signatures (fewer parameters)
- ✅ Clear ownership (player data vs world data)

**In Chapter 6**, you'll work with the dialogue system where NPCs respond to player choices.

**In later chapters**, you might create more classes:
- `NPC` class for character behavior
- `Quest` class for quest logic
- `Item` class for special item effects
- `Enemy` class for combat

You've learned a fundamental programming pattern that scales from simple games to massive projects!

---

## Chapter 5.5 Checklist

Before moving on, make sure you can:

- [ ] Explain what a class is and why it's useful
- [ ] Create a class with `__init__` and attributes
- [ ] Understand what `self` means and when to use it
- [ ] Create objects from a class
- [ ] Access object attributes with dot notation
- [ ] Refactor existing code to use a class
- [ ] Update all references when refactoring
- [ ] Test that refactored code still works correctly
- [ ] Decide when to use classes vs simple variables

**All checked?** You're ready to build more complex features! 🎯

---

## Final Thoughts

Refactoring can feel tedious - you're changing code that already works. But this is **professional software development**:

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler

By organizing your code with classes, you've made it:
- **Easier to read** - Related data is grouped
- **Easier to extend** - Add new features without tangling code
- **Easier to debug** - Clear where data lives
- **Easier to collaborate** - Other developers understand structure

**This is the difference between hobbyist code and professional code.**

You just leveled up as a programmer! 🎉

**Next:** In Chapter 6, we'll explore dialogue trees and learn how to create branching conversations with NPCs.

---

*"First make it work, then make it beautiful, then if you really, really have to, make it fast."* - Joe Armstrong
