### PLAYER CLASS ###
class Player:

    # Initial player stats 
    def __init__(self):
        self.hp = 3
        self.food = 3
        self.morale = 3

    # Get current stats as string
    def get_stats_as_string(self):
        return f"Player stats:\n- {self.hp} HP\n- {self.food} FOOD\n- {self.morale} MORALE"

    # Update stats
    def apply_effects(self, hp=0, food=0, morale=0):
        self.hp += hp
        self.food += food
        self.morale += morale

    # Check if player is alive
    def is_alive(self):
        return self.hp > 0
    
### MAIN GAME ###
# Global variables
NUM_DAYS = 10

current_day = 1
player = Player()

# Main Game Loop
while current_day <= NUM_DAYS:
    print(f"=== Day {current_day} ===")

    if current_day == 1:
        print(f"--- End of day {current_day} ---")
        print(player.get_stats_as_string())
        break

    # Placeholder for future choice logic
    # choice = input("Swipe Left (L) or Right (R)? ")
    
    print(f"--- End of day {current_day} ---\n")
    current_day += 1