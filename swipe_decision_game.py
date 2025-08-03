import random

### PLAYER CLASS ###
class Player:

    # Initial player stats 
    def __init__(self):
        self.hp = 3
        self.food = 2
        self.morale = 2

        self.low_food = 0
        self.low_morale = 0

    # Get current stats as string
    def get_stats_as_string(self):
        return f"\nPlayer stats:\n- {self.hp} HP\n- {self.food} FOOD\n- {self.morale} MORALE"

    # Update stats
    def apply_effects(self, hp=0, food=0, morale=0):
        self.hp += hp
        self.food += food
        self.morale += morale

    # Check if player is alive
    def is_alive(self):
        return self.hp > 0
    
    # Check for player food and morale
    def are_food_and_morale_low(self, food_days, morale_days):
        if self.food <= 0:
            self.low_food += 1
        if self.morale <= 0:
            self.low_morale += 1

        return self.low_food >= food_days or self.low_morale >= morale_days


###  SCENARIOS ###
scenarios = [
    {
        "description": "You find an abandoned hut with food.",
        "left_choice": {
            "text": "Search the hut",
            "effects": {"hp": 0, "food": +1, "morale": +1}
        },
        "right_choice": {
            "text": "Ignore it and move on",
            "effects": {"hp": 0, "food": 0, "morale": -1}
        }
    },
    {
        "description": "A mischievous goblin offers to trade a 'lucky rock' for some of your food.",
        "left_choice": {
            "text": "Trade your food for the rock",
            "effects": {"hp": 0, "food": -1, "morale": +2}
        },
        "right_choice": {
            "text": "Refuse and chase the goblin away",
            "effects": {"hp": 0, "food": 0, "morale": -1}
        }
    },
    {
        "description": "You come across a sparkling pond said to heal those who drink from it.",
        "left_choice": {
            "text": "Drink from the pond",
            "effects": {"hp": +2, "food": -1, "morale": +1}
        },
        "right_choice": {
            "text": "Avoid it, fearing a curse",
            "effects": {"hp": 0, "food": 0, "morale": -1}
        }
    },
    {
        "description": "A wounded knight asks for your help on the roadside.",
        "left_choice": {
            "text": "Help the knight and share your food",
            "effects": {"hp": -1, "food": -1, "morale": +2}
        },
        "right_choice": {
            "text": "Ignore the knight and move on",
            "effects": {"hp": 0, "food": 0, "morale": -2}
        }
    },
    {
        "description": "You discover a hidden chest half-buried in the forest floor.",
        "left_choice": {
            "text": "Open the chest",
            "effects": {"hp": -1, "food": +2, "morale": +1}
        },
        "right_choice": {
            "text": "Leave it untouched",
            "effects": {"hp": 0, "food": 0, "morale": 0}
        }
    }
]


### MAIN GAME ###
# Global variables
NUM_DAYS = 10

current_day = 1
player = Player()

# Main Game Loop
while current_day <= NUM_DAYS:
    print(f"=== Day {current_day} ===\n")

    scenario = random.choice(scenarios)
    print(scenario["description"])
    print("L: ", scenario["left_choice"]["text"])
    print("R: ", scenario["right_choice"]["text"])

    # Get player choice and check for input validation
    player_choice = ""
    while player_choice not in ["L", "R"]:
        player_choice = input("Swipe Left (L) or Right (R)? ").strip().upper()

    if player_choice == "L":
        effect = scenario["left_choice"]["effects"]
    else:
        effect = scenario["right_choice"]["effects"]

    # Applay effects and check survival
    player.apply_effects(**effect)
    if not player.is_alive() or player.are_food_and_morale_low(2, 2):
        print("You have perished... Game Over!")
        break
    print(player.get_stats_as_string())
    
    # End of the day
    print(f"\n--- End of day {current_day} ---\n")
    if current_day == NUM_DAYS:
        print("Congratulations! You survived the journey!")
        break
    current_day += 1