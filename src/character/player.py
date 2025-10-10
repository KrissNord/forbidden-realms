class Player:
    def __init__(self, name="Adventurer"):
        # Identity
        self.name = name
        self.gender = None
        self.race = None
        self.character_class = None
        self.background = None
        self.level = 1

        # Primary Stats (base values before modifiers)
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

        # Combat state (current values)
        self.current_health = None  # Set to max after character creation
        self.current_mana = None
        self.current_stamina = None

    # PRIMARY STAT CALCULATIONS (base + modifiers)

    def get_strength(self, race_data=None, class_data=None, background_data=None):
        """Calculate final strength with all modifiers"""
        total = self.base_strength
        if race_data and "stat_bonuses" in race_data:
            total += race_data["stat_bonuses"].get("strength", 0)
        if class_data and "stat_bonuses" in class_data:
            total += class_data["stat_bonuses"].get("strength", 0)
        if background_data and "stat_bonuses" in background_data:
            total += background_data["stat_bonuses"].get("strength", 0)
        return total

    def get_agility(self, race_data=None, class_data=None, background_data=None):
        """Calculate final agility with all modifiers"""
        total = self.base_agility
        if race_data and "stat_bonuses" in race_data:
            total += race_data["stat_bonuses"].get("agility", 0)
        if class_data and "stat_bonuses" in class_data:
            total += class_data["stat_bonuses"].get("agility", 0)
        if background_data and "stat_bonuses" in background_data:
            total += background_data["stat_bonuses"].get("agility", 0)
        return total

    def get_intelligence(self, race_data=None, class_data=None, background_data=None):
        """Calculate final intelligence with all modifiers"""
        total = self.base_intelligence
        if race_data and "stat_bonuses" in race_data:
            total += race_data["stat_bonuses"].get("intelligence", 0)
        if class_data and "stat_bonuses" in class_data:
            total += class_data["stat_bonuses"].get("intelligence", 0)
        if background_data and "stat_bonuses" in background_data:
            total += background_data["stat_bonuses"].get("intelligence", 0)
        return total

    def get_vitality(self, race_data=None, class_data=None, background_data=None):
        """Calculate final vitality with all modifiers"""
        total = self.base_vitality
        if race_data and "stat_bonuses" in race_data:
            total += race_data["stat_bonuses"].get("vitality", 0)
        if class_data and "stat_bonuses" in class_data:
            total += class_data["stat_bonuses"].get("vitality", 0)
        if background_data and "stat_bonuses" in background_data:
            total += background_data["stat_bonuses"].get("vitality", 0)
        return total

    def get_wisdom(self, race_data=None, class_data=None, background_data=None):
        """Calculate final wisdom with all modifiers"""
        total = self.base_wisdom
        if race_data and "stat_bonuses" in race_data:
            total += race_data["stat_bonuses"].get("wisdom", 0)
        if class_data and "stat_bonuses" in class_data:
            total += class_data["stat_bonuses"].get("wisdom", 0)
        if background_data and "stat_bonuses" in background_data:
            total += background_data["stat_bonuses"].get("wisdom", 0)
        return total

    def get_charisma(self, race_data=None, class_data=None, background_data=None):
        """Calculate final charisma with all modifiers"""
        total = self.base_charisma
        if race_data and "stat_bonuses" in race_data:
            total += race_data["stat_bonuses"].get("charisma", 0)
        if class_data and "stat_bonuses" in class_data:
            total += class_data["stat_bonuses"].get("charisma", 0)
        if background_data and "stat_bonuses" in background_data:
            total += background_data["stat_bonuses"].get("charisma", 0)
        return total

    def get_luck(self, race_data=None, class_data=None, background_data=None):
        """Calculate final luck with all modifiers"""
        total = self.base_luck
        if race_data and "stat_bonuses" in race_data:
            total += race_data["stat_bonuses"].get("luck", 0)
        if class_data and "stat_bonuses" in class_data:
            total += class_data["stat_bonuses"].get("luck", 0)
        if background_data and "stat_bonuses" in background_data:
            total += background_data["stat_bonuses"].get("luck", 0)
        return total

    # SECONDARY STAT CALCULATIONS (derived from primaries)

    def get_max_health(self, race_data=None, class_data=None, background_data=None):
        """Calculate maximum health"""
        vit = self.get_vitality(race_data, class_data, background_data)
        str_bonus = self.get_strength(race_data, class_data, background_data)
        return (vit * 15) + (str_bonus * 2) + (self.level * 10)

    def get_max_mana(self, race_data=None, class_data=None, background_data=None):
        """Calculate maximum mana"""
        int_stat = self.get_intelligence(race_data, class_data, background_data)
        wis = self.get_wisdom(race_data, class_data, background_data)
        return (int_stat * 10) + (wis * 5) + (self.level * 5)

    def get_max_stamina(self, race_data=None, class_data=None, background_data=None):
        """Calculate maximum stamina"""
        vit = self.get_vitality(race_data, class_data, background_data)
        agi = self.get_agility(race_data, class_data, background_data)
        return (vit * 8) + (agi * 3) + (self.level * 5)

    def get_attack_power(self, race_data=None, class_data=None, background_data=None):
        """Calculate attack power (before weapon)"""
        str_stat = self.get_strength(race_data, class_data, background_data)
        return str_stat + (str_stat // 5)

    def get_magic_power(self, race_data=None, class_data=None, background_data=None):
        """Calculate magic power"""
        int_stat = self.get_intelligence(race_data, class_data, background_data)
        return int_stat + (int_stat // 4)

    def get_defense(self, race_data=None, class_data=None, background_data=None):
        """Calculate defense (before armor)"""
        agi = self.get_agility(race_data, class_data, background_data)
        vit = self.get_vitality(race_data, class_data, background_data)
        return (agi // 3) + (vit // 4)

    def get_crit_chance(self, race_data=None, class_data=None, background_data=None):
        """Calculate critical hit chance percentage"""
        agi = self.get_agility(race_data, class_data, background_data)
        luk = self.get_luck(race_data, class_data, background_data)
        return 5 + (agi // 5) + (luk // 3)

    def get_crit_damage(self, race_data=None, class_data=None, background_data=None):
        """Calculate critical damage multiplier percentage"""
        str_stat = self.get_strength(race_data, class_data, background_data)
        luk = self.get_luck(race_data, class_data, background_data)
        return 150 + (str_stat // 4) + (luk // 5)

    def get_carry_weight(self, race_data=None, class_data=None, background_data=None):
        """Calculate maximum carry weight in kg"""
        str_stat = self.get_strength(race_data, class_data, background_data)
        vit = self.get_vitality(race_data, class_data, background_data)
        return 25 + (str_stat * 2) + vit

    def get_movement_speed(self, race_data=None, class_data=None, background_data=None):
        """Calculate movement speed percentage"""
        agi = self.get_agility(race_data, class_data, background_data)
        return 100 + (agi * 2)

    def get_mana_regen(self, race_data=None, class_data=None, background_data=None):
        """Calculate mana regeneration per turn"""
        wis = self.get_wisdom(race_data, class_data, background_data)
        int_stat = self.get_intelligence(race_data, class_data, background_data)
        return (wis // 2) + (int_stat // 5)

    def get_health_regen(self, race_data=None, class_data=None, background_data=None):
        """Calculate health regeneration per turn"""
        vit = self.get_vitality(race_data, class_data, background_data)
        wis = self.get_wisdom(race_data, class_data, background_data)
        return (vit // 3) + (wis // 4)

    def initialize_current_stats(self, race_data=None, class_data=None, background_data=None):
        """Set current HP/MP/Stamina to max after character creation"""
        self.current_health = self.get_max_health(race_data, class_data, background_data)
        self.current_mana = self.get_max_mana(race_data, class_data, background_data)
        self.current_stamina = self.get_max_stamina(race_data, class_data, background_data)
