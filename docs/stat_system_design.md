# Forbidden Realms - Stat System Design

## Primary Stats (Base: 10, Modified by Race/Class/Background)

### STR (Strength)
- **Affects:** Melee damage, carry weight, physical checks
- **Used by:** Warriors, physical combat builds
- **Example bonuses:** +2 Dwarf, +3 Warrior

### AGI (Agility)
- **Affects:** Dodge chance, initiative, ranged attacks, movement speed
- **Used by:** Rogues, ranged builds
- **Example bonuses:** +2 Elf, +3 Rogue

### INT (Intelligence)
- **Affects:** Spell damage, mana pool, learning speed, crafting quality
- **Used by:** Mages, crafters
- **Example bonuses:** +2 Elf, +3 Mage

### VIT (Vitality)
- **Affects:** Health pool, stamina, poison/disease resistance
- **Used by:** All builds (survival stat)
- **Example bonuses:** +2 Dwarf, +1 Warrior

### WIS (Wisdom)
- **Affects:** Healing effectiveness, perception, mana regeneration, dialogue insights
- **Used by:** Clerics, support builds, social interactions
- **Example bonuses:** +1 Human, +2 Scholar background

### CHA (Charisma)
- **Affects:** Merchant prices, persuasion, companion affection gain, leadership
- **Used by:** Social builds, party leaders
- **Example bonuses:** +1 Human, +2 Noble background

### LUK (Luck)
- **Affects:** Critical hit chance, loot quality, random events, quest rewards
- **Used by:** All builds (wildcard stat)
- **Example bonuses:** +1 Halfling, +1 Gambler background

---

## Secondary Stats (Calculated from Primaries)

### Combat Stats

**Health (HP)**
- Formula: `(VIT × 15) + (STR × 2) + (level × 10)`
- Why: High vitality is primary, strength helps, level scales

**Mana (MP)**
- Formula: `(INT × 10) + (WIS × 5) + (level × 5)`
- Why: Intelligence is primary source, wisdom aids, level scales

**Stamina (SP)**
- Formula: `(VIT × 8) + (AGI × 3) + (level × 5)`
- Why: For special moves, dodges, sprinting

**Attack Power**
- Formula: `STR + (weapon_damage) + (STR // 5)`
- Why: Strength is main factor, bonus every 5 points

**Magic Power**
- Formula: `INT + (INT // 4)`
- Why: Intelligence with bonus every 4 points

**Defense**
- Formula: `(AGI // 3) + (VIT // 4) + armor_value`
- Why: Agility (dodge) + vitality (toughness) + gear

**Critical Chance (%)**
- Formula: `5 + (AGI // 5) + (LUK // 3)`
- Why: Base 5%, agility precision, luck randomness

**Critical Damage (%)**
- Formula: `150 + (STR // 4) + (LUK // 5)`
- Why: 1.5x base, strength, luck

### Utility Stats

**Carry Weight (lbs)**
- Formula: `50 + (STR × 5) + (VIT × 2)`
- Why: Base human capacity + strength primary

**Movement Speed**
- Formula: `100 + (AGI × 2)`
- Why: Base speed (%), agility increases

**Mana Regeneration (per turn)**
- Formula: `(WIS // 2) + (INT // 5)`
- Why: Wisdom primary, intelligence helps

**Health Regeneration (per turn)**
- Formula: `(VIT // 3) + (WIS // 4)`
- Why: Vitality primary, wisdom aids healing

### Social Stats

**Persuasion Bonus**
- Formula: `CHA + (INT // 5)`
- Why: Charisma primary, intelligence helps arguments

**Intimidation Bonus**
- Formula: `STR + (CHA // 3)`
- Why: Physical presence + force of personality

**Deception Bonus**
- Formula: `CHA + (AGI // 4)`
- Why: Charm + quick thinking

**Barter Modifier (%)**
- Formula: `100 - (CHA × 2) - (LUK // 2)`
- Why: Lower is better (discount), charisma negotiates, luck helps

**Companion Affection Rate**
- Formula: `1.0 + (CHA / 20)`
- Why: Multiplier (1.0 = normal), charisma increases gain rate

### Crafting Stats

**Craft Quality Bonus (%)**
- Formula: `(INT // 3) + (WIS // 4)`
- Why: Knowledge + practical wisdom

**Gathering Yield Bonus (%)**
- Formula: `(LUK // 2) + (WIS // 5)`
- Why: Luck finds more, wisdom knows where to look

---

## Base Stat Values

**Default starting stats (before modifiers):** 10 for all primary stats

**Total modifier budget:**
- Race: +6 points distributed (can be negative for some stats)
- Class: +8 points distributed
- Background: +3 points distributed

**Example Human Warrior with Soldier background:**
```
Base:       STR: 10, AGI: 10, INT: 10, VIT: 10, WIS: 10, CHA: 10, LUK: 10
Human:      STR: +1, AGI: +0, INT: +0, VIT: +1, WIS: +1, CHA: +2, LUK: +1
Warrior:    STR: +3, AGI: +1, INT: +0, VIT: +3, WIS: +0, CHA: +0, LUK: +1
Soldier:    STR: +1, AGI: +0, INT: +0, VIT: +1, WIS: +0, CHA: +1, LUK: +0
---------------------------------------------------------------------------
Final:      STR: 15, AGI: 11, INT: 10, VIT: 15, WIS: 11, CHA: 13, LUK: 12

Secondary Stats (level 1):
- HP: (15×15) + (15×2) + 10 = 265
- MP: (10×10) + (11×5) + 5 = 160
- Attack: 15 + 0 + 3 = 18
- Defense: 3 + 3 + 0 = 6
- Crit Chance: 5% + 2% + 4% = 11%
```

---

## Race Bonuses (Examples)

### Human
- Versatile, balanced
- STR +1, VIT +1, WIS +1, CHA +2, LUK +1
- Total: +6

### Elf
- Graceful, intelligent
- AGI +3, INT +2, WIS +1, CHA +1, STR -1
- Total: +6

### Dwarf
- Tough, strong
- STR +2, VIT +3, WIS +1, AGI -1, CHA +1
- Total: +6

### Orc
- Powerful, intimidating
- STR +3, VIT +2, INT -1, CHA -1, LUK +1
- Total: +4 (compensated by higher base in combat stats)

---

## Class Bonuses (Examples)

### Warrior
- STR +3, AGI +1, VIT +3, LUK +1
- Starting items: Iron Sword, Leather Armor, Health Potion ×2

### Mage
- INT +4, WIS +2, VIT +1, AGI +1
- Starting items: Wooden Staff, Robe, Mana Potion ×2

### Rogue
- AGI +4, LUK +2, STR +1, CHA +1
- Starting items: Dagger, Lockpicks, Smoke Bomb ×2

---

## Background Bonuses (Examples)

### Soldier
- STR +1, VIT +1, CHA +1
- Special item: Military Badge (improves reputation with guards)

### Scholar
- INT +1, WIS +2
- Special item: Ancient Tome (improves learning speed)

### Criminal
- AGI +1, LUK +1, CHA +1
- Special item: Thieves' Tools (improves lockpicking)

---

## Stat Display Format

```
=== Character Stats ===

PRIMARY STATS:
  Strength:     15  [████████████░░░░░░░░]
  Agility:      11  [████████░░░░░░░░░░░░]
  Intelligence: 10  [███████░░░░░░░░░░░░░]
  Vitality:     15  [████████████░░░░░░░░]
  Wisdom:       11  [████████░░░░░░░░░░░░]
  Charisma:     13  [██████████░░░░░░░░░░]
  Luck:         12  [█████████░░░░░░░░░░░]

COMBAT:
  Health:       265 / 265
  Mana:         160 / 160
  Stamina:      147 / 147
  Attack:       18
  Magic Power:  12
  Defense:      6
  Crit Chance:  11%
  Crit Damage:  153%

UTILITY:
  Carry Weight: 105 / 105 lbs
  Move Speed:   122%
```

---

## Implementation Notes

### Player Class Structure
```python
class Player:
    def __init__(self):
        # Identity
        self.name = "Adventurer"
        self.gender = None
        self.race = None
        self.character_class = None
        self.background = None
        self.level = 1

        # Primary Stats (base values)
        self.base_strength = 10
        self.base_agility = 10
        self.base_intelligence = 10
        self.base_vitality = 10
        self.base_wisdom = 10
        self.base_charisma = 10
        self.base_luck = 10

        # Game state
        self.current_location = "village_entrance"
        self.gold = 0
        self.inventory = []
        self.active_quests = {}

    def get_stat(self, stat_name):
        """Calculate final stat with all modifiers"""
        # Sum: base + race + class + background + equipment

    def get_health(self):
        """Calculate max health from stats"""

    def get_mana(self):
        """Calculate max mana from stats"""
```

### Calculation Flow
1. Load race/class/background YAML files
2. Apply modifiers to base stats
3. Calculate secondary stats from modified primaries
4. Display in character sheet
5. Use in combat/checks/etc.

---

## Future Expansion

- Equipment stat bonuses
- Temporary buffs/debuffs
- Leveling system (stat points per level)
- Skills that scale with stats
- Stat requirements for equipment/abilities
- Diminishing returns at high values

---

## Testing Checklist

- [ ] Create 3 different builds
- [ ] Verify stat calculations are correct
- [ ] Ensure secondary stats update when primaries change
- [ ] Test edge cases (very high/low stats)
- [ ] Validate race/class/background combinations
