class Player:
    def __init__(self, name="Adventurer"):
        self.name = name
        self.current_location = "village_entrance"
        self.gold = 0
        self.inventory = []
        self.active_quests = {}
