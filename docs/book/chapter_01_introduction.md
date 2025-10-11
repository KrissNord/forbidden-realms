# Chapter 1: Introduction to Text-Based RPGs

## Welcome, Adventurer

You're about to embark on a journey to build **Forbidden Realms** - a complete text-based role-playing game. Not a toy example. Not a tutorial that stops at "Hello World". A **real game** with:

- A persistent world you can explore
- NPCs with branching dialogue
- A quest system with objectives and rewards
- Character creation with stats and classes
- An inventory system
- Combat mechanics
- Crafting and gathering
- Save/load functionality

And you're going to build it **all yourself**.

---

## Why Text-Based Games in 2025?

**"Aren't text games ancient history?"**

Not at all. Text-based games teach you something no flashy 3D tutorial can: **how to design systems that work together**.

Consider this: When you implement a combat system in Forbidden Realms, you'll need to:
- Calculate damage from character stats
- Check inventory for healing items
- Update quest progress when enemies are defeated
- Save the player's health after battle
- Display results with styled text

**Every system connects.** This is real software architecture.

**Other reasons text games are perfect for learning:**

✅ **Immediate Feedback** - Type a command, see results instantly

✅ **Pure Logic** - No fighting with graphics libraries or physics engines

✅ **Imagination Required** - "A rusty sword lies on the ground" beats a low-poly 3D model

✅ **Actually Fun** - You'll *want* to play your game (and so will others)

✅ **Portfolio Ready** - This is a real project you can show employers

---

## What You'll Build: Forbidden Realms

**The Elevator Pitch:**
A text-based RPG where players create characters, explore a fantasy world, complete quests, fight monsters, craft items, and make meaningful choices.

**The Technical Stack:**
- **Python 3.10+** - Modern, readable, powerful
- **Rich** - Beautiful terminal output (colors, tables, panels)
- **PyYAML** - Data-driven design (no hardcoded content)

**The Progression:**

```
Milestone 0: The Foundation
→ World exploration, locations, NPCs, save/load

Milestone 1: Life in the World
→ Dialogue trees, quest system, inventory

Milestone 2: Character Depth
→ Stats, races, classes, backgrounds, character creation

Milestone 3-10: Advanced Features
→ Combat, merchants, companions, crafting, and more
```

**By the end of this book**, you'll have a game friends will actually play.

---

## What You Need to Know

**Required Knowledge:**
- Basic Python syntax (variables, functions, loops)
- Comfortable with dictionaries and lists
- Can read error messages without panicking

**Don't worry if you're fuzzy on:**
- Object-oriented programming (we'll learn together)
- File I/O (we'll cover it)
- Game design (you'll discover it)

**The Learning Approach:**

This book follows a specific method:

1. **I explain** a concept briefly (what, why, when)
2. **I show** a small, isolated example (2-3 lines)
3. **I pose** the problem: "How would we use this for...?"
4. **You implement** it (with skeleton code + TODOs)
5. **I guide** with questions if you get stuck
6. **We debug** together when things break

**Important:** I will NOT dump complete solutions on you. If you see TODO comments, you're expected to think and implement. This is how you actually learn.

---

## Setting Up Your Environment

### Step 1: Check Python Version

Open your terminal and run:

```bash
python --version
```

You should see **Python 3.10 or higher**. If not, download it from [python.org](https://python.org).

### Step 2: Create Your Project Directory

```bash
mkdir forbidden-realms
cd forbidden-realms
```

This is your workspace. All code goes here.

### Step 3: Create a Virtual Environment

**What's a virtual environment?**
A isolated Python installation for this project. Keeps dependencies separate from other projects.

**Why use one?**
Prevents version conflicts. Libraries for this project won't interfere with other projects.

**How to create:**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt now.

### Step 4: Install Libraries

```bash
pip install rich pyyaml
```

**What these do:**
- **Rich** - Beautiful terminal formatting (colors, tables, panels, progress bars)
- **PyYAML** - Load game data from YAML files (cleaner than JSON, easier than XML)

### Step 5: Create Your First File

```bash
# On macOS/Linux:
touch main.py

# On Windows:
type nul > main.py

# Or simply open your code editor and save an empty file named main.py
```

Open `main.py` in your favorite code editor. Let's write some code!

---

## Your First Challenge: Hello, Forbidden Realms

**Objective:** Use the Rich library to display styled text in your terminal.

**Why start here?** You need to see that Python can produce beautiful output. This builds confidence and makes your game feel professional from day one.

### Concept: The Console Object

Rich uses a `Console` object to print styled text:

```python
from rich.console import Console

console = Console()
console.print("Hello!", style="bold cyan")
```

**Key points:**
- Import `Console` from `rich.console`
- Create a console instance
- Use `.print()` with a `style` parameter

**Available styles:**
- Colors: `red`, `green`, `blue`, `cyan`, `yellow`, `magenta`
- Modifiers: `bold`, `italic`, `underline`
- Combine: `bold red`, `italic cyan`

### The Challenge

Create a program that displays the game title in styled text.

**Requirements:**
1. Import Console from rich.console
2. Create a console instance
3. Print "FORBIDDEN REALMS" in bold cyan
4. Print "A Text-Based RPG Adventure" in white
5. Print a welcome message in green

**Skeleton Code:**

Open `main.py` and add this:

```python
# TODO: Import Console from rich.console


# TODO: Create a console instance


# TODO: Print the game title in bold cyan
# Hint: console.print("YOUR TEXT", style="bold cyan")


# TODO: Print the subtitle in white


# TODO: Print a welcome message in green
# Example: "Welcome, brave adventurer!"

```

### Testing

Run your program:

```bash
python main.py
```

**Expected output:**
- Game title in bright cyan, bold
- Subtitle in white
- Welcome message in green
- All nicely formatted

**Did it work?** Congratulations! You just made your game 10x more professional.

**Didn't work?** Check:
- Did you activate the virtual environment?
- Did you install rich? (`pip install rich`)
- Any typos in the import?

---

## Leveling Up: Panels and Formatting

Now that you can print styled text, let's make it look even better with **panels**.

### Concept: Rich Panels

Panels draw boxes around content:

```python
from rich.panel import Panel

console.print(Panel("This text is in a box!",
                    title="My Panel",
                    border_style="cyan"))
```

**Parameters:**
- **First argument:** Content to display
- **title:** Text shown at the top of the box
- **border_style:** Color of the border

### Mini-Challenge: ASCII Art Title

Many text games have ASCII art titles. Let's create one!

**Task:** Create a file called `title.txt` with ASCII art for your game.

**Option 1: Simple**
```
================================
    FORBIDDEN REALMS
================================
```

**Option 2: Fancy** (This shows "FORBIDDEN" - you can add "REALMS" below it)
```
███████╗ ██████╗ ██████╗ ██████╗ ██╗██████╗ ██████╗ ███████╗███╗   ██╗
██╔════╝██╔═══██╗██╔══██╗██╔══██╗██║██╔══██╗██╔══██╗██╔════╝████╗  ██║
█████╗  ██║   ██║██████╔╝██████╔╝██║██║  ██║██║  ██║█████╗  ██╔██╗ ██║
██╔══╝  ██║   ██║██╔══██╗██╔══██╗██║██║  ██║██║  ██║██╔══╝  ██║╚██╗██║
██║     ╚██████╔╝██║  ██║██████╔╝██║██████╔╝██████╔╝███████╗██║ ╚████║
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝

██████╗ ███████╗ █████╗ ██╗     ███╗   ███╗███████╗
██╔══██╗██╔════╝██╔══██╗██║     ████╗ ████║██╔════╝
██████╔╝█████╗  ███████║██║     ██╔████╔██║███████╗
██╔══██╗██╔══╝  ██╔══██║██║     ██║╚██╔╝██║╚════██║
██║  ██║███████╗██║  ██║███████╗██║ ╚═╝ ██║███████║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
```

**Where to get fancy ASCII art:** [patorjk.com/software/taag](https://patorjk.com/software/taag/)

### Challenge: Load and Display ASCII Art

**Requirements:**
1. Create a `data` directory
2. Create `data/ascii/title.txt` with your ASCII art
3. Modify `main.py` to:
   - Read the file contents
   - Display it in a panel with cyan border

**Skeleton:**

```python
# After your previous code, add:

# TODO: Read the ASCII art file
# Hint: with open("data/ascii/title.txt", "r") as file:
#           content = file.read()


# TODO: Display it in a panel
# Hint: console.print(Panel(content, border_style="cyan"))

```

**Testing:**
```bash
python main.py
```

You should see your ASCII art in a beautiful cyan-bordered panel!

---

## The Game Loop Concept

Every game has a **game loop** - code that runs repeatedly until the player quits.

**The pattern:**

```python
while True:
    # 1. Show current state
    # 2. Get player input
    # 3. Process the command
    # 4. Update game state
    # 5. Repeat
```

**Simple example:**

```python
while True:
    command = console.input("[bold white]> [/bold white]")

    if command == "quit":
        console.print("[green]Thanks for playing![/green]")
        break
    elif command == "help":
        console.print("Commands: help, quit", style="blue")
    else:
        console.print(f"Unknown command: {command}", style="red")
```

**Key concepts:**
- `while True:` loops forever
- `break` exits the loop
- `console.input()` gets styled input (vs plain `input()`)
- Get input → process → repeat

### Final Challenge: Basic Game Loop

Add a simple game loop to your program.

**Requirements:**
1. After displaying the title, start a loop
2. Show a prompt: `> `
3. If player types "quit", exit
4. If player types "help", show available commands
5. Otherwise, say "Unknown command"

**Skeleton:**

```python
# After displaying the title panel:

# TODO: Create the game loop
while True:
    # TODO: Get player input
    # Hint: command = console.input("[bold white]> [/bold white]")


    # TODO: Handle quit command
    # if command == "quit":
    #     console.print("[green]Thanks for playing![/green]")
    #     break


    # TODO: Handle help command
    # elif command == "help":
    #     console.print("Commands: help, quit", style="blue")


    # TODO: Handle unknown commands
    # else:
    #     console.print(f"Unknown command: {command}", style="red")

```

**Test it:**
```bash
python main.py
```

Try:
- `help` → Should show commands
- `asdf` → Should say unknown command
- `quit` → Should exit

---

## What You've Learned

✅ **Rich library basics** - Styled console output

✅ **File I/O** - Reading files with `open()`

✅ **Game loops** - The fundamental pattern of interactive programs

✅ **User input** - Getting and processing commands

✅ **Environment setup** - Virtual environments and dependencies

---

## Looking Ahead

In Chapter 2, you'll learn:
- **YAML data files** - Representing game content
- **Dictionaries and lists** - The building blocks of game data
- **Your first location** - Creating a place players can explore

By the end of Chapter 2, you'll be able to `look` around and see a description of where you are. The world is coming to life!

---

## Extension Ideas

Want to go further? Try these:

### Extension 1: Color Customization
Add a settings system where players can choose their favorite color scheme.

### Extension 2: Animated Text
Make text appear character-by-character (like old terminals).
Hint: Look up `time.sleep()` and looping through strings.

### Extension 3: Multiple Title Screens
Create different ASCII art for different moods (day/night, seasons, etc.) and randomly choose one.

---

## Debugging Corner

### Error: `ModuleNotFoundError: No module named 'rich'`
**Cause:** Rich not installed, or virtual environment not activated.

**Fix:**
```bash
# Make sure venv is activated (you should see (venv) in prompt)
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# Install rich
pip install rich
```

### Error: `FileNotFoundError: [Errno 2] No such file or directory: 'data/ascii/title.txt'`
**Cause:** File doesn't exist or wrong path.

**Fix:**
- Make sure you created the `data/ascii/` directories
- Check the file is named exactly `title.txt`
- Check you're running from the right directory (`forbidden-realms/`)

### Output looks weird / no colors
**Cause:** Your terminal might not support colors.

**Fix:**
- Try a different terminal (Windows Terminal, iTerm2, etc.)
- Or use `console.print(content)` without styles

---

## Chapter 1 Checklist

Before moving on, make sure you can:

- [ ] Run Python 3.10+ on your system
- [ ] Create and activate a virtual environment
- [ ] Install packages with pip
- [ ] Print styled text with Rich
- [ ] Read files from disk
- [ ] Display content in panels
- [ ] Create a basic game loop
- [ ] Process player commands

**All checked?** You're ready for Chapter 2! 🎮

---

## Final Thoughts

You just wrote your first game code. It might not seem like much - a title screen and a loop - but you've established the foundation:

✅ **Beautiful output** - Your game looks professional
✅ **Game loop structure** - The heartbeat of interactive programs
✅ **File loading** - Content separated from code
✅ **User interaction** - Commands and responses

Every complex game is built on these same foundations. You're on your way.

**Next:** In Chapter 2, we'll add real game content using YAML files. You'll create your first location and learn how to represent a world in data.

---

*"The journey of a thousand lines begins with a single function."* - Ancient Developer Proverb

