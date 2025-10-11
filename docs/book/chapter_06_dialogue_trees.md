# Chapter 6: Dialogue Trees - Conversations with NPCs

## The Problem: Static NPCs

Right now, your NPCs are just names in YAML files. They exist in locations, but they don't do anything:

```yaml
# data/locations/village_entrance.yaml
npcs:
  - guard_tom
```

**This is boring.** Players can't interact with them, learn from them, or get quests. They're just decorative.

**What we want:**
- Branching conversations with multiple choices
- Different responses based on player input
- NPCs that give quests, hints, backstory
- Conversations that feel natural and engaging

**The solution:** Dialogue trees - structured conversations where each choice leads to different branches.

---

## What You'll Learn

By the end of this chapter:
- ✅ Design branching conversations with node-based structure
- ✅ Create dialogue files in YAML format
- ✅ Implement dialogue navigation (following choices)
- ✅ Display NPC text and player choices
- ✅ Handle terminal nodes (conversation endings)
- ✅ Integrate dialogue with quests

---

## Concept: What Are Dialogue Trees?

A **dialogue tree** is like a "Choose Your Own Adventure" book:

```
[NPC]: "Welcome, traveler!"

  → [1] "Hello! What's this place?"
      [NPC]: "This is Runewild Village..."

  → [2] "I'm looking for work."
      [NPC]: "Ah, an adventurer! We do have a problem..."

  → [3] "Goodbye."
      [NPC]: "Safe travels."
      [END]
```

**Key concepts:**
- **Nodes** - Each piece of NPC dialogue
- **Choices** - Options the player can pick
- **Branches** - Different paths based on choices
- **Terminal nodes** - Conversation endings (no more choices)

### Visual Example

```
              greeting
             /    |    \
          /       |       \
       /          |          \
   friendly    neutral      rude
      |           |           |
   follow-up   follow-up    [END]
      |           |
    [END]       [END]
```

Each node contains:
- NPC's dialogue text
- List of player choices
- Where each choice leads (next node)

---

## Understanding Node-Based Dialogue

Before we code, let's design a simple dialogue on paper.

### Example: Meeting a Guard

**Node: greeting** (starting point)
- **NPC says:** "Halt! State your business."
- **Player choices:**
  1. "Just passing through." → goes to `passing_through` node
  2. "I'm looking for work." → goes to `work_inquiry` node
  3. "None of your business!" → goes to `rude_response` node

**Node: passing_through**
- **NPC says:** "Fair enough. Move along."
- **Player choices:** (none - conversation ends)

**Node: work_inquiry**
- **NPC says:** "We have a rat problem at the mill. Interested?"
- **Player choices:**
  1. "Sure, I'll help." → goes to `quest_accept` node
  2. "Rats? No thanks." → goes to `quest_decline` node

**Node: quest_accept**
- **NPC says:** "Great! The mill is east of here."
- **Trigger:** Start the "Rat Problem" quest
- **Player choices:** (none - conversation ends)

**Key insight:** Each node knows its text, choices, and where choices lead. The dialogue system just follows the path!

---

## Challenge 1: Your First Dialogue File

Let's create a simple dialogue for an NPC.

### Step 1: Create the NPC Directory

```bash
mkdir -p data/npcs
```

### Step 2: Create Your First NPC

Create `data/npcs/merchant_sara.yaml`:

**Skeleton:**

```yaml
name: Merchant Sara

dialogues:
  # This is the starting node - always called "greeting"
  greeting:
    text: "Welcome to my shop! Looking for supplies?"
    choices:
      # TODO: Add first choice - "What do you sell?"
      # Format:
      #   - text: "Player's dialogue line"
      #     goes_to: node_id_to_go_to


      # TODO: Add second choice - "Just browsing."
      # Goes to: browse_response


  # TODO: Create the "wares" node
  # This node lists what she sells
  # wares:
  #   text: "I sell potions, tools, and maps. Reasonable prices!"
  #   choices:
  #     # Add a choice to ask about potions (goes_to: potions)
  #     # Add a choice to say goodbye (goes_to: farewell)


  # TODO: Create the "potions" node
  # potions:
  #   text: "Health potions are 25 gold each. Restore 50 HP instantly!"
  #   choices:
  #     # Add a choice to buy (goes_to: buy_potion)
  #     # Add a choice to decline (goes_to: no_thanks)


  # TODO: Create the "browse_response" node
  # browse_response:
  #   text: "Take your time! Let me know if you need anything."
  #   choices: []  # Empty list means conversation ends


  # TODO: Create the "farewell" node
  # farewell:
  #   text: "Come back anytime!"
  #   choices: []


  # TODO: Create the "buy_potion" node
  # buy_potion:
  #   text: "Here you go! Use it wisely."
  #   choices: []


  # TODO: Create the "no_thanks" node
  # no_thanks:
  #   text: "No problem. Anything else?"
  #   choices:
  #     # Add choice to ask about wares again
  #     # Add choice to say goodbye
```

### Step 3: Understanding the Structure

**Node format:**

```yaml
node_name:
  text: "What the NPC says"
  choices:
    - text: "Player's response"
      goes_to: next_node_name
    - text: "Another player response"
      goes_to: different_node_name
```

**Terminal node (conversation ending):**

```yaml
farewell:
  text: "Goodbye!"
  choices: []  # Empty list - no more choices
```

### Guiding Questions

**Q1: What if I create a choice that goes to a node that doesn't exist?**

<details>
<summary>Hint</summary>

This will cause an error when the player tries that choice! The dialogue system will look for the node and not find it.

**Example of broken dialogue:**

```yaml
greeting:
  text: "Hello!"
  choices:
    - text: "Goodbye"
      goes_to: farewell  # But you never created the "farewell" node!
```

**Good practice:** Always create the nodes you reference!

You can use the validators from Chapter 4 to check for this automatically.
</details>

**Q2: What's special about the "greeting" node?**

<details>
<summary>Hint</summary>

The `greeting` node is where every conversation starts. When a player types `talk merchant_sara`, the dialogue system loads the NPC's dialogue and starts at the `greeting` node.

Think of it as the "main()" function for dialogue!
</details>

**Q3: Can multiple choices lead to the same node?**

<details>
<summary>Hint</summary>

Yes! This is useful for converging paths:

```yaml
greeting:
  text: "Want to buy something?"
  choices:
    - text: "Yes!"
      goes_to: show_wares
    - text: "Sure, let me see."
      goes_to: show_wares  # Same destination
    - text: "Maybe later."
      goes_to: farewell
```

Different ways of saying yes can lead to the same outcome.
</details>

---

## Challenge 2: Implement the Dialogue System

Now let's write Python code to navigate these dialogue trees.

### Concept: Following the Path

**The algorithm:**

```
1. Load the NPC's dialogue data from YAML
2. Start at the "greeting" node
3. Display the NPC's text
4. If node has choices:
   a. Display all choices (numbered)
   b. Get player input
   c. Find which choice was selected
   d. Go to that choice's `goes_to` node
   e. Repeat from step 3
5. If node has no choices:
   - Conversation ends
```

### Step 1: Load NPCs at Startup

In `main.py`, add NPC loading:

```python
# After loading locations
import os

# TODO: Load all NPCs
npcs = {}
for filename in os.listdir("data/npcs"):
    if filename.endswith(".yaml"):
        # TODO: Get NPC ID from filename
        # Hint: npc_id = filename.replace(".yaml", "")


        # TODO: Load the NPC file
        # Hint: with open(f"data/npcs/{filename}", "r") as file:
        #           npc_data = yaml.safe_load(file)


        # TODO: Add to npcs dictionary
        # Hint: npcs[npc_id] = npc_data
```

### Step 2: Implement the talk Command

Add the `talk` command to your game loop:

```python
elif action == "talk":
    # TODO: Check if player specified an NPC
    if len(parts) < 2:
        console.print("Talk to whom?", style="red")
    else:
        # TODO: Get NPC name from command
        # Hint: npc_input = "_".join(parts[1:]).lower()


        # TODO: Get current location data
        current_loc_data = locations[player.current_location]

        # TODO: Check if NPC is in this location
        if npc_input in current_loc_data["npcs"]:

            # TODO: Check if NPC data exists
            if npc_input in npcs:

                # TODO: Start dialogue
                # Call a function: run_dialogue(npc_input, npcs[npc_input], console)
                pass

            else:
                console.print(f"[red]NPC data not found for {npc_input}[/red]")

        else:
            console.print(f"[red]There's no {npc_input} here.[/red]")
```

### Step 3: Implement the Dialogue Engine

Create a new file `src/helpers/dialogue.py`:

**Skeleton:**

```python
def run_dialogue(npc_id, npc_data, console):
    """
    Run a dialogue conversation with an NPC.

    Args:
        npc_id: ID of the NPC (e.g., "merchant_sara")
        npc_data: Dictionary with NPC name and dialogues
        console: Rich console for display
    """
    from rich.panel import Panel

    # TODO: Get NPC name
    npc_name = npc_data["name"]

    # TODO: Get all dialogue nodes
    dialogues = npc_data["dialogues"]

    # TODO: Start at greeting node
    current_node = "greeting"

    # TODO: Loop until conversation ends
    while True:

        # TODO: Get current node data
        if current_node not in dialogues:
            console.print(f"[red]Dialogue node '{current_node}' not found![/red]")
            break

        node_data = dialogues[current_node]

        # TODO: Display NPC's dialogue in a panel
        # Hint: console.print(Panel(
        #           node_data["text"],
        #           title=f"[bold cyan]{npc_name}[/bold cyan]",
        #           border_style="cyan"
        #       ))


        # TODO: Check if node has choices
        if not node_data.get("choices"):
            # No choices - conversation ends
            break

        # TODO: Display player choices
        console.print("\n[bold yellow]Your response:[/bold yellow]")
        for i, choice in enumerate(node_data["choices"], 1):
            # TODO: Print each choice with number
            # Hint: console.print(f"  {i}. {choice['text']}", style="bright_white")


        # TODO: Get player input
        # Hint: user_input = console.input("[bold cyan]> [/]")


        # TODO: Validate input is a number
        try:
            choice_num = int(user_input)
        except ValueError:
            console.print("[red]Please enter a number.[/red]")
            continue

        # TODO: Check if choice number is valid
        if 1 <= choice_num <= len(node_data["choices"]):

            # TODO: Get selected choice
            selected_choice = node_data["choices"][choice_num - 1]

            # TODO: Move to next node
            current_node = selected_choice["goes_to"]

        else:
            console.print("[red]Invalid choice. Try again.[/red]")
```

### Step 4: Import and Use

In `main.py`, add the import:

```python
from src.helpers.dialogue import run_dialogue
```

And in the `talk` command, call it:

```python
run_dialogue(npc_input, npcs[npc_input], console)
```

---

## Challenge 3: Test Your Dialogue System

**Test plan:**

1. **Start game and find NPC**
   - ✅ NPC appears in location
   - ✅ `talk merchant_sara` starts dialogue

2. **Follow dialogue path**
   - ✅ NPC text displays in panel
   - ✅ Choices are numbered
   - ✅ Entering a number follows that choice
   - ✅ Next node loads correctly

3. **Reach terminal node**
   - ✅ Conversation ends when no choices
   - ✅ Returns to game loop

4. **Test error cases**
   - ✅ `talk nonexistent` shows error
   - ✅ Typing non-number shows error
   - ✅ Typing invalid number (0, 99) shows error

5. **Test multiple paths**
   - ✅ Different choices lead to different nodes
   - ✅ Can have multiple conversations
   - ✅ Can revisit same NPC

---

## Understanding Dialogue State

Right now, every conversation starts from `greeting`. But what if you want NPCs to remember previous conversations?

### Concept: Dialogue State Tracking

```python
# In your Player class (from Chapter 5.5)
class Player:
    def __init__(self, starting_location):
        self.current_location = starting_location
        self.inventory = []
        self.dialogue_state = {}  # Track NPC conversation progress

# When player completes a quest:
player.dialogue_state["guard_tom"] = "quest_complete"

# In dialogue YAML:
greeting:
  text: "{% if dialogue_state.guard_tom == 'quest_complete' %}You're back! Did you clear the mill?{% else %}Halt! State your business.{% endif %}"
```

**Note:** This is an advanced topic we'll cover more in later chapters. For now, all conversations start fresh each time.

---

## Extension: Quest Integration

You can trigger quests from dialogue! Add this to a node:

```yaml
quest_accept:
  text: "Great! The mill is east of here. Good luck!"
  trigger_quest: rat_problem  # This starts the quest!
  choices: []
```

**In your dialogue engine, check for trigger_quest:**

```python
# After moving to new node, check for quest trigger
if "trigger_quest" in node_data:
    quest_id = node_data["trigger_quest"]
    # TODO: Add quest to player.active_quests
    # (We'll implement this fully in Chapter 7)
    console.print(f"\n[green]Quest started: {quest_id}[/green]")
```

---

## Common Mistakes

### Mistake 1: Forgetting terminal nodes need empty choices

```yaml
# WRONG - no choices field
farewell:
  text: "Goodbye!"

# RIGHT - explicit empty list
farewell:
  text: "Goodbye!"
  choices: []
```

### Mistake 2: goes_to pointing to non-existent node

```yaml
# WRONG
greeting:
  text: "Hello!"
  choices:
    - text: "Bye"
      goes_to: farwell  # TYPO! Should be "farewell"

# RIGHT
greeting:
  text: "Hello!"
  choices:
    - text: "Bye"
      goes_to: farewell  # Correct spelling
```

**How to prevent:** Use validation! Check all `goes_to` targets exist.

### Mistake 3: Infinite loops with no exit

```yaml
# WRONG - player is trapped!
node_a:
  text: "Something"
  choices:
    - text: "Continue"
      goes_to: node_b

node_b:
  text: "Something else"
  choices:
    - text: "Go back"
      goes_to: node_a  # Loops back, no way to exit!

# RIGHT - always provide an exit
node_b:
  text: "Something else"
  choices:
    - text: "Go back"
      goes_to: node_a
    - text: "Goodbye"
      goes_to: farewell  # Exit path
```

### Mistake 4: Not handling invalid input

```python
# WRONG - crashes on non-number
choice_num = int(user_input)  # ValueError if user types "abc"

# RIGHT - use try/except
try:
    choice_num = int(user_input)
except ValueError:
    console.print("Please enter a number.", style="red")
    continue
```

---

## Extension Ideas

### Extension 1: Validate Dialogue Files

Create a validator (like Chapter 4) to check:
- All `goes_to` targets exist
- Every dialogue tree has a `greeting` node
- No infinite loops without exits
- All required fields are present

### Extension 2: Dialogue Shortcuts

Allow players to type `talk guard` instead of `talk guard_tom` if unambiguous:

```python
# Find NPCs whose ID contains the input
matches = [npc for npc in current_loc_data["npcs"] if npc_input in npc]
if len(matches) == 1:
    npc_id = matches[0]
elif len(matches) > 1:
    console.print(f"Ambiguous! Did you mean: {', '.join(matches)}")
else:
    console.print("No such NPC here.")
```

### Extension 3: Dialogue History

Track which nodes the player has seen:

```python
player.dialogue_history["merchant_sara"] = ["greeting", "wares", "potions"]

# Then show different greeting if returning
if "greeting" in player.dialogue_history.get("merchant_sara", []):
    # Returning player
    current_node = "return_greeting"
else:
    # First time meeting
    current_node = "greeting"
```

### Extension 4: Rich Choice Display

Use Rich panels for choices:

```python
from rich.table import Table

table = Table(show_header=False, box=None)
for i, choice in enumerate(node_data["choices"], 1):
    table.add_row(f"[bold cyan]{i}[/bold cyan]", choice['text'])
console.print(table)
```

---

## Debugging Corner

### Error: `KeyError: 'greeting'`

**Cause:** Your NPC's dialogue doesn't have a `greeting` node.

**Fix:** Every NPC needs a `greeting` node as the starting point:

```yaml
dialogues:
  greeting:  # This is required!
    text: "Hello!"
    choices: []
```

### Error: `KeyError: 'some_node'`

**Cause:** A choice has `goes_to: some_node` but that node doesn't exist in the dialogue.

**Debug:**
```python
# Print all node names in dialogue
print(dialogues.keys())  # See what nodes exist
```

**Fix:** Either create the missing node or fix the `goes_to` reference.

### Bug: Conversation starts but choices don't work

**Possible cause:** Your choice handling logic has a bug.

**Debug:**
```python
# Add debug prints
print(f"Player chose: {choice_num}")
print(f"Valid range: 1 to {len(node_data['choices'])}")
print(f"Selected: {selected_choice}")
```

### Bug: Conversation never ends

**Cause:** You're not checking for empty choices list, or node is missing `choices: []`.

**Fix:**
```python
# Make sure you have this check
if not node_data.get("choices"):
    # No choices = conversation ends
    break
```

---

## What You've Learned

✅ **Dialogue tree structure** - Nodes, choices, branches

✅ **YAML dialogue format** - text, choices, goes_to

✅ **Node-based navigation** - Following paths through dialogue

✅ **Terminal nodes** - Ending conversations

✅ **Input validation** - Handling invalid player input

✅ **Error handling** - Checking for missing nodes

✅ **Quest integration** - Triggering quests from dialogue

---

## Looking Ahead

**In Chapter 7**, you'll implement a complete quest system:
- Quest objectives (kill X, collect Y, talk to Z)
- Quest progress tracking
- Quest rewards
- Quest states (active, complete, failed)

Dialogue trees will trigger quests, and quests will affect dialogue!

---

## Chapter 6 Checklist

Before moving on, make sure you can:

- [ ] Design a dialogue tree on paper (nodes, choices, paths)
- [ ] Create dialogue YAML files with proper structure
- [ ] Load NPC data at game startup
- [ ] Implement the `talk` command
- [ ] Navigate through dialogue nodes
- [ ] Display NPC text and player choices
- [ ] Handle terminal nodes (conversation endings)
- [ ] Validate player input (number checking)
- [ ] Debug missing node errors
- [ ] Identify and fix infinite dialogue loops

**All checked?** Your NPCs can now talk! 🗣️

---

## Final Thoughts

Dialogue trees are the heart of story-driven games. Look at any RPG:

- **The Witcher**: Complex branching conversations with consequences
- **Mass Effect**: Dialogue wheel with personality choices
- **Undertale**: Dialogue that changes based on player actions
- **Your game**: The foundation is the same!

The structure you've built is **professional-grade**:
- Data-driven (easy to add new NPCs)
- Flexible (any conversation structure)
- Extensible (add quest triggers, conditions, etc.)

**Next steps in the book will add:**
- Conditional dialogue (different text based on player state)
- Dialogue that checks inventory, quests, stats
- Personality-based responses
- Timed dialogue choices

You're building a real RPG dialogue system, not a toy example!

**Next:** In Chapter 7, we'll create quests that NPCs give through dialogue.

---

*"Dialogue is character, and character is plot."* - Wes Anderson
