# Chapter 4: Validation - Keeping Your World Consistent

## The Silent Killer: Bad Data

You've built an explorable world with locations and movement. But here's a scary scenario:

**You create a new location:**
```yaml
# data/locations/haunted_forest.yaml
name: Haunted Forest
exits:
  west: old_mill
  south: vilage_entrance  # TYPO! Should be "village_entrance"
```

**What happens when a player tries to go south?**

```
> go south
Traceback (most recent call last):
  File "main.py", line 42, in <module>
    current_location = locations[new_location_id]
KeyError: 'vilage_entrance'
```

**CRASH.** Game over. Player loses progress.

**The problem:** You won't discover this typo until a player tries to move south in the Haunted Forest. That could be hours into the game!

**The solution:** **Validators** - code that checks your data files for errors **before** anyone plays.

---

## What Is Validation?

**Validation** is checking that your data makes sense **before** it's used.

**Examples of things to validate:**

❌ **Broken exits** - Do all exits point to locations that exist?

❌ **Orphaned locations** - Are there unreachable locations (you can't get to them from anywhere)?

❌ **Missing NPCs** - Do locations reference NPCs that don't exist?

❌ **Missing items** - Do locations reference items that don't exist?

❌ **Circular dependencies** - Does location A need B, which needs C, which needs A?

**When to validate:** At startup, **before** the player can do anything.

**If validation fails:** Report errors clearly, then **refuse to start the game**.

Why refuse? Because a broken game is worse than no game. Better to show the developer (you!) what's wrong than let players encounter crashes.

---

## Concept: Cross-Reference Checking

**Cross-reference** means "does this reference point to something that exists?"

**Example:**

```yaml
# Location references an NPC
npcs:
  - guard_tom
```

**The validator asks:**
- Does `guard_tom` exist in the NPCs dictionary?
- If not → ERROR: "Location 'village_entrance' references missing NPC 'guard_tom'"

**Pattern:**

```python
for location_id, location_data in locations.items():
    for npc_id in location_data["npcs"]:
        if npc_id not in npcs:
            print(f"ERROR: Location '{location_id}' references missing NPC '{npc_id}'")
```

---

## Challenge 1: Validate Exits

Let's build your first validator - checking that all exits point to real locations.

### Step 1: Create a Validators Module

Create `src/helpers/validators.py`:

```bash
mkdir -p src/helpers
touch src/helpers/validators.py
```

**Why a separate module?**
- Keeps main.py clean
- Validators are reusable
- Easy to add more validators later

### Step 2: Understand the Logic

**For each location:**
1. Get its exits dictionary
2. For each exit (direction → destination):
   - Check if destination exists in locations dictionary
   - If not → record an error

**For all errors collected:**
- If any errors exist → print them and return False
- If no errors → return True

**Return value matters:** `True` means "validation passed, safe to continue". `False` means "errors found, don't start the game".

### Step 3: Implement the Validator

**Requirements:**
- Function name: `validate_exits`
- Parameters: `locations` (dict), `console` (for styled output), `settings` (for print_styled)
- Returns: `True` if valid, `False` if errors found

**Skeleton:**

```python
# src/helpers/validators.py

from .display import print_styled


def validate_exits(locations, console, settings):
    """
    Validate that all exits point to locations that exist.

    Args:
        locations: Dictionary of all location data
        console: Rich console for output
        settings: Game settings (for styled printing)

    Returns:
        bool: True if valid, False if errors found
    """
    has_errors = False

    # TODO: Loop through all locations
    for location_id, location_data in # ???:

        # TODO: Get the exits dictionary


        # TODO: Loop through each exit
        for direction, destination in # ???:

            # TODO: Check if destination exists in locations
            if destination in locations:
                pass  # Valid exit, all good
            else:
                # TODO: Print error message
                # Hint: print_styled(console, settings,
                #           f"ERROR: Location '{location_id}' has exit '{direction}'
                #              pointing to missing location '{destination}'",
                #           style="red")


                # TODO: Mark that we found an error
                has_errors = # ???

    # TODO: Return True if no errors, False if errors found
    return # ???
```

### Guiding Questions

**Q1: How do I loop through dictionary items (key-value pairs)?**

<details>
<summary>Hint</summary>

```python
for key, value in dictionary.items():
    print(key, value)
```

In our case:
```python
for location_id, location_data in locations.items():
    # location_id is "village_entrance"
    # location_data is the dictionary with name, description, exits, etc.
```
</details>

**Q2: How do I check if a key exists in a dictionary?**

<details>
<summary>Hint</summary>

```python
if "village_entrance" in locations:
    # The key exists!
```

Or for variables:
```python
if destination in locations:
    # The destination location exists
```
</details>

**Q3: Why use `has_errors` instead of returning immediately?**

<details>
<summary>Hint</summary>

We want to report **ALL** errors, not just the first one.

If we did this:
```python
if destination not in locations:
    print("ERROR")
    return False  # Stop immediately
```

We'd only see one error and miss others.

Instead, we collect all errors, then return at the end.
</details>

---

## Challenge 2: Call the Validator

Now that you have a validator, let's use it!

### Step 1: Import the Validator

In `main.py`, add the import:

```python
from src.helpers.validators import validate_exits
from src.helpers.display import print_styled
```

### Step 2: Call It Before Starting

**Where to call it:** After loading all locations, **before** the game loop starts.

**Pattern:**

```python
# ... load all locations ...

# Validate before starting
if validate_exits(locations, console, settings):
    # Validation passed - start the game
    console.clear()
    # ... show title ...
    # ... game loop ...
else:
    # Validation failed - don't start
    print_styled(console, settings, "Validation failed. Fix errors before playing.", style="red")
    sys.exit()
```

**Key insight:** The `if` statement acts as a **gatekeeper**. If validation fails, the game never starts.

### Your Task: Add Validation

Modify `main.py` to call the validator.

**Skeleton:**

```python
import sys  # Add this at the top if not there

# ... loading code ...

# TODO: Call validator
if # ???:
    # TODO: Validation passed - continue to game

    console.clear()
    # ... title screen ...
    # ... game loop ...

else:
    # TODO: Validation failed - report and exit


```

---

## Challenge 3: Test Your Validator

Let's intentionally break something to see if the validator catches it!

### Test 1: Create a broken exit

Edit `data/locations/village_entrance.yaml`:

```yaml
exits:
  north: town_square
  south: nonexistent_place  # This location doesn't exist!
```

**Run the game:**

```bash
python main.py
```

**Expected output:**
```
ERROR: Location 'village_entrance' has exit 'south' pointing to missing location 'nonexistent_place'
Validation failed. Fix errors before playing.
```

**Did it work?** ✅ Your validator caught the bug!

**Fix the exit** back to a valid location before continuing.

### Test 2: Multiple errors

Create a new location with multiple broken exits:

```yaml
# data/locations/test_broken.yaml
name: Test Location
exits:
  north: fake_place
  south: another_fake
  west: village_entrance  # This one is valid
npcs: []
items: []
```

**Run again:**

You should see **two** error messages (one for each broken exit). This proves your validator reports ALL errors, not just the first.

**Delete the test file** after testing.

---

## Concept: Sets and Set Operations

Before we dive into graph connectivity, let's learn about **sets** - a powerful Python data structure perfect for validation.

### What Are Sets?

A **set** is like a list, but:
- **No duplicates** - Each element appears once
- **Unordered** - No indexes like `set[0]`
- **Fast membership checking** - `if x in my_set` is very fast
- **Set operations** - Union, intersection, difference

**Creating sets:**

```python
# From a list (duplicates removed automatically)
items = {"apple", "banana", "apple"}  # Only one "apple" kept
print(items)  # {"apple", "banana"}

# Empty set
visited = set()

# From a list
numbers = set([1, 2, 2, 3])  # {1, 2, 3}
```

### Set Operations for Validation

Sets are perfect for comparing what **should exist** vs what **actually exists**.

**Example 1: Finding missing NPCs**

```python
# NPCs referenced in locations
referenced_npcs = set()
for location in locations.values():
    for npc in location["npcs"]:
        referenced_npcs.add(npc)  # Add to set

# NPCs that actually exist
existing_npcs = set(npcs.keys())

# Find NPCs that are referenced but don't exist
missing_npcs = referenced_npcs - existing_npcs

# Report errors
for npc in missing_npcs:
    print(f"ERROR: NPC '{npc}' is referenced but doesn't exist")
```

**Example 2: Finding unused items**

```python
# Items that exist
all_items = set(items.keys())  # {"wooden_branch", "health_potion", "sword"}

# Items actually used in locations
used_items = set()
for location in locations.values():
    for item in location["items"]:
        used_items.add(item)

# Items that exist but are never used
unused = all_items - used_items
print(f"Warning: These items are defined but never appear: {unused}")
```

**Example 3: Finding locations with no exits**

```python
# Locations with at least one exit
locations_with_exits = set()
for location_id, location_data in locations.items():
    if location_data["exits"]:  # If exits dict is not empty
        locations_with_exits.add(location_id)

# All locations
all_locations = set(locations.keys())

# Dead-ends (might be intentional, but worth checking)
dead_ends = all_locations - locations_with_exits
for location in dead_ends:
    print(f"Note: '{location}' has no exits (dead-end)")
```

### Key Set Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union (all elements in either set)
a | b  # {1, 2, 3, 4, 5, 6}

# Intersection (elements in both sets)
a & b  # {3, 4}

# Difference (in a but not in b)
a - b  # {1, 2}

# Symmetric difference (in a or b, but not both)
a ^ b  # {1, 2, 5, 6}
```

**For validation, we mostly use subtraction (-) to find missing elements.**

---

## Concept: Graph Connectivity

Here's a subtle bug validators can catch:

**You create a location that can't be reached:**

```yaml
# data/locations/secret_room.yaml
name: Secret Room
exits:
  west: village_entrance
# ... but no location has an exit TO secret_room!
```

This location exists, but **you can't get there**. It's orphaned!

**Graph theory** helps us find unreachable locations.

### Understanding Graphs

Your world is a **graph**:
- **Nodes** = Locations
- **Edges** = Exits

```
Village Entrance --north--> Town Square
     ^                          |
     |                          |
   south                       west
     |                          |
     +-------- Old Mill <-------+
```

**Graph connectivity** means: "Can I reach every node from the starting node?"

**Algorithm** (breadth-first search):

```
1. Start at the beginning location
2. Mark it as visited
3. Look at all its exits
4. For each exit, if not visited yet:
   - Mark as visited
   - Add to "to visit" list
5. Repeat until no more locations to visit
6. Compare visited locations to ALL locations
7. Any location not visited = unreachable
```

---

## Challenge 4: Validate Graph Connectivity

Implement a validator that finds unreachable locations.

**This is the most complex validator**, but you can do it! Let's break it down.

### Step 1: Understand the Algorithm (Visual Walkthrough)

**Imagine this world:**

```
    town_square -------- market
         |                  |
       north              west
         |                  |
  village_entrance --east-- old_mill

  secret_room  (orphaned - no connections!)
```

**BFS explores level by level, like ripples in water:**

```
Initial State:
  visited = {}
  to_visit = [village_entrance]  ← Start here

─────────────────────────────────────────
Round 1: Process village_entrance

  ✓ Mark village_entrance as visited
  ✓ Look at exits: {north: town_square, east: old_mill}
  ✓ Add unvisited neighbors to queue

  visited = {village_entrance}
  to_visit = [town_square, old_mill]

─────────────────────────────────────────
Round 2: Process town_square

  ✓ Mark town_square as visited
  ✓ Look at exits: {south: village_entrance, north: market}
  ✓ village_entrance already visited (skip)
  ✓ market not visited (add to queue)

  visited = {village_entrance, town_square}
  to_visit = [old_mill, market]

─────────────────────────────────────────
Round 3: Process old_mill

  ✓ Mark old_mill as visited
  ✓ Look at exits: {west: village_entrance, north: market}
  ✓ Both already visited or in queue (skip)

  visited = {village_entrance, town_square, old_mill}
  to_visit = [market]

─────────────────────────────────────────
Round 4: Process market

  ✓ Mark market as visited
  ✓ Look at exits: {south: town_square, east: old_mill}
  ✓ Both already visited (skip)

  visited = {village_entrance, town_square, old_mill, market}
  to_visit = []  ← Empty! We're done

─────────────────────────────────────────
Final Check:

  all_locations = {village_entrance, town_square, old_mill, market, secret_room}
  visited = {village_entrance, town_square, old_mill, market}

  unreachable = all_locations - visited
             = {secret_room}

  ❌ ERROR: secret_room is unreachable!
```

**Key insight:** BFS guarantees we find ALL reachable locations. Anything left over is unreachable.

### Step 2: Implement the Validator

**Before we code:** This algorithm uses `.pop(0)` on a list to create a queue. For small games (< 100 locations), this works fine. For larger games, consider using `collections.deque` which is faster. We'll keep it simple for now!

**Skeleton:**

```python
def validate_graph_connectivity(locations, console, settings):
    """
    Check that all locations are reachable from the starting location.

    Uses breadth-first search (BFS) to find all reachable locations,
    then compares to the full list.

    Args:
        locations: Dictionary of all location data
        console: Rich console for output
        settings: Game settings

    Returns:
        True if all locations reachable, False if any unreachable
    """
    if not locations:
        return True  # No locations = nothing to validate

    # TODO: Set starting location
    # (This should be where the player starts the game)
    starting_location = "village_entrance"

    # TODO: Create sets for visited and to_visit queue
    visited = set()  # Locations we've already explored
    to_visit = [starting_location]  # Queue of locations to check (FIFO)

    # TODO: While there are locations to visit
    # Hint: while to_visit:
    while # ???:

        # TODO: Get next location from queue
        # Hint: current_location_id = to_visit.pop(0)  # Take first element


        # TODO: Mark as visited
        # Hint: visited.add(current_location_id)


        # TODO: Get the location's data
        # Hint: current_location_data = locations[current_location_id]


        # TODO: Look at all exits
        # for direction, destination in # ???:

            # TODO: If destination not visited AND not in to_visit queue
            # if destination not in visited and destination not in to_visit:

                # TODO: Add to queue
                # to_visit.append(destination)


    # TODO: Get set of all locations
    all_locations = set(locations.keys())

    # TODO: Find unreachable locations
    # unreachable = all_locations - visited  # Set subtraction


    # TODO: Report errors
    has_errors = False
    for location in # ???:
        # TODO: Print error


        has_errors = True

    return not has_errors
```

### Guiding Questions

**Q1: What's a set and why use it?**

<details>
<summary>Hint</summary>

A **set** is like a list, but:
- No duplicates allowed
- Very fast membership checking (`if x in my_set`)
- Supports set operations (union, intersection, difference)

```python
visited = set()
visited.add("village_entrance")
visited.add("village_entrance")  # Duplicate ignored
print(visited)  # {"village_entrance"}
```

**Why use it here?** We need to track "have I visited this location?" - sets are perfect for this.
</details>

**Q2: What does `.pop(0)` do?**

<details>
<summary>Hint</summary>

Removes and returns the **first** element of a list:

```python
queue = ["a", "b", "c"]
first = queue.pop(0)  # first = "a"
# queue is now ["b", "c"]
```

This creates a **queue** (FIFO - First In, First Out), which is what we need for breadth-first search.
</details>

**Q3: What is set subtraction?**

<details>
<summary>Hint</summary>

`a - b` gives you elements in `a` that are NOT in `b`:

```python
all_locations = {"a", "b", "c", "d"}
visited = {"a", "b"}
unreachable = all_locations - visited  # {"c", "d"}
```

Perfect for finding locations we never reached!
</details>

---

## Testing Graph Connectivity

### Test 1: All locations reachable (should pass)

Make sure your locations are all connected:

```
Village Entrance <--> Town Square <--> Old Mill
```

Run the game - should start normally.

### Test 2: Add an unreachable location

Create `data/locations/isolated_room.yaml`:

```yaml
name: Isolated Room
description: You can't get here from anywhere!
exits: {}
npcs: []
items: []
```

**Run the game:**

Should show: `ERROR: Location 'isolated_room' is unreachable.`

**This is good!** The validator caught the problem before a player could get confused.

---

## Putting It All Together

Now your game startup looks like this:

```python
# Load data
locations = load_all_locations()
npcs = load_all_npcs()

# Validate everything
if (validate_exits(locations, console, settings) and
    validate_graph_connectivity(locations, console, settings) and
    validate_npcs(locations, npcs, console, settings)):

    # All validations passed - safe to play!
    start_game()

else:
    # At least one validation failed
    print("Fix errors before playing")
    sys.exit()
```

**Benefits:**

✅ Catches typos before they cause crashes

✅ Finds unreachable content (so you don't waste time creating it)

✅ Reports ALL errors at once (fix them all, then test)

✅ Gives you confidence your world is consistent

---

## What You've Learned

✅ **Why validation matters** - Catch bugs early, before players see them

✅ **Cross-reference checking** - Verify references point to real data

✅ **Graph algorithms** - Breadth-first search for connectivity

✅ **Sets** - Fast membership checking and set operations

✅ **Queues** - FIFO data structures with `.pop(0)`

✅ **Boolean operators** - Combining multiple conditions with `and`

✅ **Error reporting** - Clear messages for developers

---

## Common Mistakes

### Mistake 1: Forgetting to check both directions

```python
# WRONG - only checks if destination exists
if destination in locations:
    # Don't also check if destination can reach back

# This misses one-way dead ends!
```

**Note:** This is actually okay for now. Some games have one-way exits (falling down a hole, etc.). Graph connectivity will catch truly isolated locations.

### Mistake 2: Returning too early

```python
# WRONG
if error:
    return False  # Stops immediately, misses other errors

# RIGHT
if error:
    has_errors = True  # Record error, keep checking
# Later...
return not has_errors
```

### Mistake 3: Modifying set while iterating

```python
# WRONG
for location in to_visit:
    to_visit.add(new_location)  # Modifying while looping!

# RIGHT - use a list for the queue
to_visit = []  # List, not set
to_visit.append(new_location)
```

### Mistake 4: Not handling empty data

```python
# What if locations is empty?
starting_location = locations["village_entrance"]  # KeyError!

# Better
if not locations:
    return True  # Nothing to validate
```

---

## Extension Ideas

### Extension 1: Validate NPCs

Create `validate_npcs(locations, npcs, console, settings)` that checks:
- Do all NPCs referenced in locations actually exist?
- Are there NPC files that are never used?

### Extension 2: Validate Items

Check that items referenced in locations exist in the items dictionary.

### Extension 3: Validate Dialogue

Check that NPC dialogue nodes are properly connected:
- Do all `goes_to` fields point to existing nodes?
- Are there orphaned dialogue nodes (never referenced)?

### Extension 4: Validation Report

Instead of printing errors directly, collect them and generate a detailed report:

```
=== Validation Report ===
✓ 12 locations loaded
✓ All exits valid
✗ 2 unreachable locations:
  - secret_room
  - abandoned_tower
✓ All NPCs valid

Result: 1 error found
```

---

## Debugging Corner

### Error: `KeyError: 'village_entrance'`

**In validator:**
```python
starting_location = "village_entrance"
```

**Cause:** Starting location doesn't exist (maybe you renamed it?)

**Fix:** Make sure your starting location actually exists in the locations dictionary, or make it configurable:

```python
# Get any location as starting point
starting_location = list(locations.keys())[0]
```

### Error: `TypeError: 'NoneType' object is not iterable`

**Cause:** A location's exits field is `None` instead of a dictionary.

**Example broken YAML:**
```yaml
exits:  # Nothing here - becomes None
npcs: []
```

**Fix:** Either provide exits or use an empty dict:
```yaml
exits: {}  # Empty dictionary
```

**Or validate it:**
```python
exits = location_data.get("exits", {})  # Default to empty dict
```

### Infinite Loop in Graph Connectivity

**Symptom:** Validator never finishes.

**Cause:** Not marking locations as visited, so they get added to queue repeatedly.

**Fix:** Make sure you're adding to the `visited` set:
```python
visited.add(current_location_id)
```

---

## Looking Ahead

In Chapter 5, you'll implement **save/load** functionality so players can quit and resume later.

You'll learn:
- JSON serialization
- File writing
- Data versioning
- What to save (and what not to save)

---

## Chapter 4 Checklist

Before moving on, make sure you can:

- [ ] Explain why validation is important
- [ ] Loop through dictionary items
- [ ] Check if a key exists in a dictionary
- [ ] Collect multiple errors before returning
- [ ] Understand basic graph concepts (nodes, edges)
- [ ] Implement breadth-first search
- [ ] Use sets for membership checking
- [ ] Use set subtraction to find missing elements
- [ ] Combine multiple validators with boolean operators

**All checked?** Your game is now robust and error-resistant! 🛡️

---

## Final Thoughts

Validation is often the least exciting part of game development, but it's one of the **most important**.

**Professional game studios** have extensive validation systems:
- Asset validators (are all textures the right size?)
- Quest validators (can every quest be completed?)
- Balance validators (is any item too powerful?)
- Build validators (does the game even run?)

**You're learning real software engineering** - not just game development. These same validation patterns apply to:
- Web forms (is the email valid?)
- APIs (does this request have all required fields?)
- Databases (do all foreign keys reference real records?)
- Configuration files (are all settings valid?)

Validation is **defensive programming** - assume things will go wrong, and catch them before they do.

**Next:** In Chapter 5, we'll make your game persistent with save/load functionality!

---

*"An ounce of validation is worth a pound of debugging."* - Ancient Developer Proverb
