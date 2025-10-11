# Building Forbidden Realms: Learn Python Through Game Development

## Table of Contents

---

## Part 1: Foundations (M0)

### Chapter 1: Introduction to Text-Based RPGs
- What makes a good text-based game?
- Overview of what we'll build
- Setting up your development environment
- Your first "Hello World" with Rich

**Concepts:** Print statements, strings, imports, libraries

**Project:** Display styled text to console

---

### Chapter 2: Data Structures - Representing Your World
- Why YAML instead of hardcoded data?
- Dictionaries: The building blocks of game data
- Lists: Managing collections
- Loading data from files

**Concepts:** Dictionaries, lists, file I/O, YAML

**Challenge:** Create your first location YAML file
**Skeleton:** Partial YAML with TODOs

---

### Chapter 3: The Game Loop
- What is a game loop?
- Getting user input
- Parsing commands (string methods)
- The main loop pattern

**Concepts:** while loops, string methods (split, strip, lower), conditionals

**Challenge:** Implement `look` and `go` commands
**Skeleton:** Loop structure with TODO command handlers

---

### Chapter 4: Validation - Keeping Your World Consistent
- Why validate data?
- Cross-reference checking (do exits point to real locations?)
- Graph traversal (is every location reachable?)
- Error reporting to developers

**Concepts:** Nested loops, sets, algorithms, error handling

**Challenge:** Implement NPC validator
**Skeleton:** Graph connectivity validator with TODOs

---

### Chapter 5: Save and Load - Preserving Player Progress
- JSON vs YAML (when to use each)
- Serializing game state
- Loading and restoring state
- Version compatibility

**Concepts:** JSON, file writing, data persistence

**Challenge:** Add player gold to save system
**Skeleton:** Save/load functions with TODOs

---

### Chapter 5.5: Refactoring to Classes - Better Code Organization
- What are classes and objects?
- Why refactor working code?
- Understanding self and methods
- Refactoring variables to a Player class
- When to use classes vs simple variables

**Concepts:** OOP basics, classes, __init__, self, refactoring, encapsulation

**Challenge:** Create Player class and refactor main.py
**Skeleton:** Player class template with TODOs

**Important:** This bridges M0 → M1. All future chapters assume you have a Player class!

---

**Milestone 0 Complete!** 🎉 You now have a playable world with organized, maintainable code!

---

## Part 2: Bringing the World to Life (M1)

### Chapter 6: Dialogue Trees - Conversations with NPCs
- Designing branching conversations
- Node-based dialogue structure
- Handling player choices
- State management (tracking dialogue progress)
- YAML dialogue format

**Concepts:** Nested dictionaries, state machines, recursion/loops

**Challenge:** Create a merchant NPC with buy/sell dialogue
**Skeleton:** Dialogue loop with TODOs for choice handling

---

### Chapter 7: Quest Systems - Giving Players Goals
- Quest structure (objectives, rewards, states)
- Triggering quests from dialogue
- Tracking quest progress
- Quest completion detection

**Concepts:** Complex data structures, state management, dictionaries within dictionaries

**Challenge:** Create a fetch quest (bring X items)
**Skeleton:** Quest tracking with TODOs

---

### Chapter 8: Inventory - Managing Items
- List operations (append, remove, in)
- Item lookup patterns
- State persistence (items in locations + player inventory)
- The "disappearing items" bug and how to fix it

**Concepts:** Lists, dictionaries, references vs copies, state management

**Challenge:** Implement the `use` command
**Skeleton:** `take` and `inventory` commands with TODOs for `use`

---

### Chapter 9: The Item System - YAML Data Files
- Creating a flexible item schema
- Loading items at startup
- Graceful fallbacks (what if item file is missing?)
- The `inspect` command

**Concepts:** Data-driven design, error handling, optional parameters

**Challenge:** Create 3 new items with effects
**Skeleton:** Item YAML template with TODOs

---

**Milestone 2 Checkpoint:** You now have NPCs, quests, and items!

---

## Part 3: Character Depth (M2)

### Chapter 10: Stats System - Numbers That Matter
- Primary stats (what they affect)
- Calculated stats (formulas from primary stats)
- Stat modifiers (race + class + background)
- The power of small numbers (balance)

**Concepts:** Arithmetic, formulas, functions with parameters

**Challenge:** Design your own secondary stat (e.g., dodge chance)
**Skeleton:** Player stat methods with TODOs

---

### Chapter 11: Character Creation Flow
- Sequential prompts
- Input validation patterns
- The try/except pattern for number input
- Looping until valid input

**Concepts:** Input validation, try/except, while loops, user experience

**Challenge:** YOU IMPLEMENT THIS (current session!)
**Skeleton:** Already created in character_creator.py

---

### Chapter 12: Races, Classes, Backgrounds
- Modular character building
- YAML-driven design choices
- Stat bonuses and starting items
- Balancing different playstyles

**Concepts:** Data-driven design, balance, player choice

**Challenge:** Create a new race with unique bonuses
**Skeleton:** Race YAML template

---

**Milestone 3 Checkpoint:** Players can create unique characters!

---

## Part 4: Advanced Topics (Future Milestones)

### Chapter 13: Combat System (M4)
### Chapter 14: Merchant and Economy (M3)
### Chapter 15: Companion System (M5)
### Chapter 16: Crafting and Gathering (M7)
### Chapter 17: Natural Language Parsing (M8)

---

## Appendices

### Appendix A: Python Quick Reference
- Data types cheat sheet
- Common patterns
- String formatting
- List/dict operations

### Appendix B: Game Design Principles
- Balancing stats
- Writing engaging dialogue
- Quest design patterns
- Player motivation

### Appendix C: Debugging Guide
- Common errors and solutions
- Reading stack traces
- Using print statements
- Validator patterns

### Appendix D: Project Reference
- Complete file structure
- YAML schemas
- Naming conventions
- Code style guide

---

## Teaching Features Throughout

Each chapter includes:

✅ **Learning Objectives** - What you'll learn
✅ **Concept Explanation** - Brief (what, why, when)
✅ **Isolated Examples** - 2-3 line code snippets
✅ **The Challenge** - What you'll build
✅ **Skeleton Code** - TODOs to guide you
✅ **Guiding Questions** - If you get stuck
✅ **Solution Discussion** - After you try (NOT full code dump)
✅ **Extension Ideas** - Take it further
✅ **Common Mistakes** - What to watch out for

---

## Book Format

- **Primary Format:** Markdown (easy to write, easy to version control)
- **Can Convert To:** PDF, HTML, EPUB later
- **Code Repository:** GitHub with progressive branches (chapter-1, chapter-2, etc.)
- **Reader Downloads:** Code at any checkpoint

---

## Book Philosophy

**What This Book IS:**
- A project-based learning experience
- Focused on understanding through building
- Challenging but supportive
- Building a REAL playable game

**What This Book IS NOT:**
- A reference manual
- A dump of complete solutions
- A passive reading experience
- Focused on memorization

---

## Next Steps

1. Write Chapter 1 together
2. Establish the chapter template
3. You write some sections, I guide
4. Build out chapters progressively
5. Test with other learners
6. Refine based on feedback

---

**Target Audience:**
- Beginners with basic Python (loops, functions, dictionaries)
- People who learn by doing
- Aspiring game developers
- Fans of text-based RPGs

**What makes this book different:**
- ACTUALLY makes you code (not just read)
- Teaches through mistakes and debugging
- Uses a real, fun project
- Respects the reader's ability to think
