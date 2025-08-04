import random
import helper_functions as hf
import list_of_scenarios as los

### PLAYER CLASS ###
class Player:

    # Initial player stats 
    def __init__(self):
        self.hp = 5
        self.food = 3
        self.morale = 3

        self.low_food = 0
        self.low_morale = 0

    # Get current stats as string
    def get_stats_as_string(self):
        return f"\nPlayer stats:\n- {self.hp} HP\n- {self.food} FOOD\n- {self.morale} MORALE"

    # Update stats
    def apply_effects(self, hp=0, food=0, morale=0):
        self.update_hp(hp)
        self.update_food(food)
        self.update_morale(morale)

    def update_hp(self, value):
        self.hp = hf.clamp(self.hp + value, 0, 5)

    def update_food(self, value):
        self.food = hf.clamp(self.food + value, 0, 8)

    def update_morale(self, value):
        self.morale = hf.clamp(self.morale + value, 0, 5)

    # Check if player is alive
    def is_alive(self):
        return self.hp > 0
    
    # Check for player food and morale + daily decay
    def daily_decay(self):
        self.update_food(-1)

        if self.food <= 0:
            self.low_food += 1
            self.update_hp(-1)
            if self.low_food % 2 == 0:
                self.update_morale(-1)
        else:
            self.low_food = 0

        if self.morale <= 0:
            self.low_morale += 1
        else:
            self.low_morale = 0

    def is_food_low(self, food_days):
        return self.low_food >= food_days
    
    def is_morale_low(self, morale_days):
        return  self.low_morale >= morale_days


###  SCENARIOS ###
scenarios = los.scenarios

### EVENT LOG ###
event_log = []
log_choice_text = ""
def event_log_update(day, scenario, choice, choice_text):
    event_log.append(f"Day {day}: {scenario['description']} -> Choice: {choice} | {choice_text}")

def final_score(num_of_days, hp, food, morale):
    return (num_of_days * 10) + (hp * 5) + (food * 2) + (morale * 5)

def print_event_log(score):
    print("\nYour journey is over. Here's what happened:")
    for event in event_log:
        print(event)
    print(f"Your final score is: {score}")


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
        chosen_option = scenario["left_choice"] 
        if "chance" in chosen_option:
            if random.random() <= chosen_option["chance"]:
                effect = chosen_option["success_effects"]
                log_choice_text = f"{chosen_option['log_text']} Success!"
            else:
                effect = chosen_option["success_effects"]
                log_choice_text = f"{chosen_option['log_text']} Failure..."
        else:
            effect = chosen_option["effects"]
            log_choice_text = chosen_option["log_text"]
    else:
        chosen_option = scenario["right_choice"] 
        effect = chosen_option["effects"]
        log_choice_text = chosen_option["log_text"]

    print("\n", log_choice_text)

    # Apply effects
    surprise = los.get_random_event()
    if surprise != -1:
        print(surprise["text"])
        player.apply_effects(surprise["hp"], surprise["food"], surprise["morale"])
        event_log.append(f"   Surprise Event: {surprise['text']}")

    player.apply_effects(**effect)
    player.daily_decay()

    # Event log
    event_log_update(current_day, scenario, player_choice, log_choice_text)
    
    # Check survival
    if not player.is_alive():
        print("You have perished... Game Over!")
        break
    if player.is_food_low(3):
        print("Your party was starving for too long... Game Over!")
        break
    if player.is_morale_low(3):
        print("Your party got depressed and disbanded... Game Over!")
        break
    
    print(player.get_stats_as_string())
    
    # End of the day
    print(f"\n--- End of day {current_day} ---\n")
    if current_day == NUM_DAYS:
        print("Congratulations! You survived the journey!")
        break
    current_day += 1

# Printing choices and final score
print_event_log(final_score(current_day, player.hp, player.food, player.morale))