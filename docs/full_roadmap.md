# Forbidden Realms — Incremental Roadmap (Priority-First)

## Guiding rules

* **Playable at every step.** Each milestone ends with a build you can start, play for 10–20 minutes, and finish a tiny loop.
* **Small vertical slices.** Add thin end-to-end experiences (content + UI + data + validation) instead of half features.
* **Dependency-aware.** Core systems first; optional features come only when prerequisites exist.
* **Feature flags.** Anything experimental ships behind a toggle so it can be disabled without removing code/content.
* **Stable content IDs.** No reuse. Save schema versioned from the start.

---

## Priority map (what comes first, and why)

1. **Core Loop (Must-have to play at all)**
   * Boot + UI skeleton (Rich + ASCII)
   * Content loading/validation from YAML
   * Exploration (locations + exits)
   * Minimal parser (look, go, talk)
   * Dialogue & one quest
   * Inventory basics (take/use), saving/loading

2. **Core RPG Feel (Makes it an RPG)**
   * Character creation (name → race → gender → appearance → class → background)
   * Stats (primary → secondary → derived)
   * Merchant/shop & gold
   * Turn combat (one family of enemies)

3. **Depth & Party (Replay hooks)**
   * Companion (recruit, dismiss, basic orders)
   * Affection (display + small deltas) and a first romance gate
   * Natural language expansion (equip, give, buy/sell patterns)

4. **Economy Loop (Satisfying progression)**
   * Gathering nodes (herbs first)
   * Crafting (alchemy first with 2–3 recipes)
   * Node cooldowns, skill influence

5. **Scale & Polish**
   * Second region (scale test)
   * Balance pass (TTK/economy/affection tuning)
   * Packaging & playtest build, monochrome mode, ASCII width audit

---

## Milestones (each produces a shippable build)

### M0 — Project Seed (v0.1.0)

**Why now:** Foundation for every other feature.

**Deliverables**
* Rich console shell; ASCII title banner (80–90 cols), version stamp.
* YAML loader + cache build; schema + cross-ref + graph validation.
* Minimal game loop; `help`, `look`, `go N/S/E/W`.
* Two locations connected; one NPC with a greeting.
* Save/load (snapshot) and settings (color on/off, text width).

**Exit criteria**
* Start → look → move → talk → save → quit works without errors.
* Validators pass; no isolated map nodes.

---

### M1 — Dialogue & First Quest (v0.2.0)

**Why now:** Establish the narrative loop before combat.

**Deliverables**
* Dialogue nodes with choices, simple conditions, and a **single side quest** (visit + talk).
* Quest log pane (compact list with status).
* Rewards grant gold + a potion (useable).

**Exit criteria**
* Accept → advance → complete the quest, see log & reward panel.
* All IDs resolve; build clean.

---

### M2 — Character Creation (v0.3.0)

**Why now:** It changes how everything feels; needed before balance work.

**Deliverables**
* Full creator: name, gender, race, appearance (scoped options), class, background.
* Stats: primary/secondary/derived; preview panel updates live.
* Starting kit by class/background.

**Exit criteria**
* Three unique builds feel distinct; stats & starting items match choices.
* Derived stats recompute correctly on start.

---

### M3 — Inventory & Merchant (v0.4.0)

**Why now:** Enables progression without combat; supports next steps.

**Deliverables**
* Take, inspect, use, equip (basic); shop buy/sell with totals.
* 10 items across potions, swords, axes, light armor, materials.
* Gold as currency; value & rarity fields respected.

**Exit criteria**
* Equipping affects secondary/derived stats (visible).
* Buy/sell loop cannot go negative; stack limits enforced.

---

### M4 — Combat Slice (v0.5.0)

**Why now:** Core RPG pillar, but only after inventory & stats are stable.

**Deliverables**
* Turn combat with initiative, basic actions (attack, defend, use item, flee).
* 2 enemy variants; one wilderness encounter table.
* Victory/defeat flows; loot and gold drops; short Rich combat frame.

**Exit criteria**
* A reliable loop: town → outskirts fight → return → shop.
* TTK target 3–5 rounds; no softlocks on flee/defeat.

---

### M5 — Companion (v0.6.0)

**Why now:** Party depth; prepares for affection & romance.

**Deliverables**
* Recruit/dismiss one companion (e.g., **Clara Runestorm**).
* Companion card in sidebar; simple behavior toggle (aggressive/defensive/support).
* Orders via NL: "Clara, defend" / "Clara, focus archer".

**Exit criteria**
* Companion persists across screens & saves.
* Orders visibly alter action choices in combat.

---

### M6 — Affection & First Romance Gate (v0.7.0)

**Why now:** Ties together dialogue, quest outcomes, and companion loops.

**Deliverables**
* Affection metric (0–100) visible on inspect; small deltas from choices/gifts.
* One gated romance scene with Clara; clear thresholds & flags.

**Exit criteria**
* Gifting works with likes/dislikes; thresholds respected; scene unlocks once.

---

### M7 — Gathering & Crafting (Alchemy) (v0.8.0)

**Why now:** Adds a satisfying, non-combat progression loop and economy sink.

**Deliverables**
* Herb nodes in 2–3 locations; tool requirement optional for now.
* 3 alchemy recipes (e.g., Minor Healing, Antidote, Focus Tonic).
* Node cooldowns; Gathering skill lightly influences yield.

**Exit criteria**
* Loop: gather → craft → use/sell; recipes consume inputs and produce outputs.
* Cooldowns prevent infinite farm in one spot.

---

### M8 — Natural Language Expansion (v0.9.0)

**Why now:** Quality of life once verbs exist.

**Deliverables**
* NL patterns for equip, give, buy/sell, craft quantities, and gathering.
* Disambiguation prompts are one-line, cancellable; confirmations concise.

**Exit criteria**
* "craft two minor healings", "give Clara a wolf pelt", "equip the iron sword" all succeed reliably.

---

### M9 — Second Region & Scale Check (v0.10.0)

**Why now:** Validate content model and performance with more data.

**Deliverables**
* New region with ASCII headers, 10+ locations, 2–3 enemy families, 5–10 items, 3–4 quests.
* Travel gate (flag or permit quest).

**Exit criteria**
* Build time remains snappy; validators still pass; no width overflows in ASCII.

---

### M10 — Balance & Packaging (v1.0.0-playtest)

**Why now:** Lock a showcase build.

**Deliverables**
* Tuning pass (combat, economy, crafting value, affection gains).
* Monochrome mode; ASCII width audit; version/changelog on title.
* Packaged executables for Win/macOS/Linux.

**Exit criteria**
* A new player can complete a 45–60 min run without hitting walls.
* Clean startup on fresh machine; saves persist; no hard crashes reported.

---

## Backlog (post-v1.0 playtest, nice-to-have)

* Smithing, Cooking, Enchanting domains.
* Multiple companions & party formation rules.
* More romance arcs and epilogues.
* Minimap glyphs; ASCII portraits (optional).
* Achievements and challenge runs.
* Difficulty modes and story-only toggle.

---

## Acceptance checklists (per milestone)

**Global**
* Validators: schema, cross-refs, world graph (no isolated nodes unless intended).
* ASCII audit: no line > 90 chars; monochrome readable.
* Save schema version increments on breaking changes; friendly incompat notice.

**Parser/NL**
* Unknown verb: suggest two likely commands + `help`.
* Unknown target: offer top 2 matches or quick disambiguation.
* Disambiguation always cancellable; no loops.

**Combat**
* Initiative respects stats; status effects apply & expire; flee has clear outcomes.
* Victory/defeat returns to stable states; loot resolves even if inventory is full (drop to ground or overflow rule).

**Companions**
* Recruit/dismiss preserved on save/load; orders reflected next combat round.
* Sidebar correctly shows health/affection.

**Crafting/Gathering**
* Node cooldown timers persist across save/load.
* Skill/tool modifiers applied consistently; failure rules (if any) documented.

---

## Release & cadence

* Tag every milestone: `0.X.0` where **X = milestone number**.
* Changelog per release with **What's New / Changed / Fixed / Known Issues / Suggested Test Route**.
* Keep **feature flags** for anything not fully validated (toggle in settings or a simple config file).

---

## Immediate next actions (to start M0 → M1 cleanly)

1. Create ASCII assets: title banner and one location header.
2. Finalize YAML schemas (including quests/dialogs) and run validators on sample content.
3. Implement minimal loop with `help`, `look`, `go`, `talk`, `save`, `load`.
4. Author **Runewild Village** hub with 4–6 locations and one NPC; wire a simple "visit + talk" quest.
5. Ship **v0.1.0**, then expand dialogue into the first real quest for **v0.2.0**.
