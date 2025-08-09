import random
import helper_functions as hf
import list_of_scenarios as los

### PLAYER CLASS ###
class Player:

    # Initial player stats 
    def __init__(self, hp=5, food=3, morale=3, hp_max=5, food_max=8, morale_max=5, difficulty="normal"):
        self.hp = hp
        self.food = food
        self.morale = morale
        self.difficulty = difficulty

        self.hp_max = hp_max
        self.food_max = food_max
        self.morale_max = morale_max

        self.low_food = 0
        self.low_morale = 0
        self.cause_of_death = "None"

    # Get current stats as string
    def get_stats_as_string(self):
        return f"\nPlayer stats:\n- {self.hp} HP ❤️\n- {self.food} FOOD 🍗\n- {self.morale} MORALE 😇"

    # Update stats
    def apply_effects(self, hp=0, food=0, morale=0):
        self.update_hp(hp)
        self.update_food(food)
        self.update_morale(morale)

    def update_hp(self, value):
        self.hp = hf.clamp(self.hp + value, 0, self.hp_max)

    def update_food(self, value):
        self.food = hf.clamp(self.food + value, 0, self.food_max)

    def update_morale(self, value):
        self.morale = hf.clamp(self.morale + value, 0, self.morale_max)

    # Check if player is alive
    def is_alive(self):
        return self.hp > 0
    
    # Check for player food and morale + daily decay
    def daily_decay(self):
        self.update_food(-1)

        if self.food <= 0:
            self.low_food += 1
            self.update_hp(-1)
            if self.low_food % diff_conf["starve_morale_every_n_days"] == 0:
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


### MAIN GAME ###
# Global variables
NUM_DAYS = 10

current_day = 1
player = Player()

diff_conf = los.DIFF_CFG["normal"]
"""
    diff_conf["starve_morale_every_n_days"]
    diff_conf["starve_morale_every_n_days"]
    diff_conf["low_food_death_days"]
    diff_conf["low_morale_death_days"]
    diff_conf["surprise_chance"]
    diff_conf["risk_success_bonus"]
"""

###  SCENARIOS ###
scenarios = los.scenarios
if NUM_DAYS > len(scenarios):
    raise ValueError("NUM_DAYS exceeds available scenarios.")
random_list_of_scenarios = random.sample(scenarios, NUM_DAYS)

### EVENT LOG ###
event_log = []
log_choice_text = ""
def event_log_update(day, scenario, choice, choice_text, effect_r):
    event_log.append(
        f"Day {day}: {scenario['description']} -> Choice: {choice} | {choice_text}"
        f"\n       (HP: {effect_r['hp']}, Food: {effect_r['food']}, Morale {effect_r['morale']})"
    )

# Final score
def final_score(num_of_days, hp, food, morale, diff):
    return ((num_of_days * 10) + (hp * 5) + (food * 2) + (morale * 5)) * diff

# End game stats
def print_event_log(score, days, death):
    print(f"\nYour journey is over, you survived for {days} days. Here's what happened:")
    for event in event_log:
        print(event)

    print("\n🌟 \033[32mAdventure Complete!\033[0m 🌟")
    print(f"  \033[32mYou survived {days} days.\033[0m")
    if death != "None":
        print(f"  \033[31mCause of death: {death}\033[0m")
    print(f"  \033[32mFinal score: {score}\033[0m")

# Global functions
# Returns the effect dict and log text based on the player's choice.
def process_player_choice(scenario, choice):
    if choice == "L":
        chosen_option = scenario["left_choice"]
    else:
        chosen_option = scenario["right_choice"]

    # Check for chance-based outcomes
    if "chance" in chosen_option:
        # Getting chance for success
        chance = hf.clamp(chosen_option["chance"] + diff_conf["risk_success_bonus"], 0.05, 0.95)
        if random.random() <= chance:
            effect = chosen_option["success_effects"]
            log_text = f"\033[32m{chosen_option['log_text']} Success!\033[0m"
        else:
            effect = chosen_option["failure_effects"]
            log_text = f"\033[31m{chosen_option['log_text']} Failure...\033[0m"
    else:
        effect = chosen_option["effects"]
        log_text = f"\033[33m{chosen_option['log_text']}\033[0m"

    return effect, log_text

def process_surprise_event():
    surprise_loc = los.get_random_event(diff_conf["surprise_chance"])
    if surprise_loc != -1:
        print(f"\033[35m{surprise_loc['text']}\033[0m")
        return surprise_loc  # return the dict with effects
    return None

def reset_globals():
    global current_day, player, event_log, log_choice_text, random_list_of_scenarios
    current_day = 1
    player = Player()
    event_log = []
    log_choice_text = ""
    random_list_of_scenarios = random.sample(scenarios, NUM_DAYS)

def choose_difficulty():
    global player, diff_conf
    difficulty = input("\nChoose difficulty: (1) Easy, (2) Normal, (3) Hard\nDifficulty: ").strip()
    if difficulty == "1":
        player = Player(hp=6, food=4, morale=4, hp_max=6, food_max=9, morale_max=6, difficulty="easy")
        diff_conf = los.DIFF_CFG["easy"]
    elif difficulty == "3":
        player = Player(hp=4, food=2, morale=2, hp_max=4, food_max=7, morale_max=4, difficulty="hard")
        diff_conf = los.DIFF_CFG["hard"]
    else:
        player = Player()
        diff_conf = los.DIFF_CFG["normal"]

def difficulty_mul(difficulty):
    if difficulty == "normal":
        return 2
    elif difficulty == "hard":
        return 3
    return 1

# Main Game Loop
while True:
    choose_difficulty()
    reset_globals()

    while current_day <= NUM_DAYS:
        print("\n" + "="*25)
        print(f"       🌄  DAY {current_day}  🌄")
        print("="*25 + "\n")

        scenario = random_list_of_scenarios[current_day-1]

        print(scenario["description"])
        print("L: ", scenario["left_choice"]["text"])
        print("R: ", scenario["right_choice"]["text"])

        # Get player choice and check for input validation
        player_choice = ""
        while player_choice not in ["L", "R"]:
            player_choice = input("Swipe Left (L) or Right (R)? ").strip().upper()

        # Get and process player choice
        effect, log_choice_text = process_player_choice(scenario, player_choice)
        print(f"\n{log_choice_text}")

        # Handle surprise event
        surprise = process_surprise_event()
        if surprise:
            player.apply_effects(surprise["hp"], surprise["food"], surprise["morale"])
            event_log.append(f" \033[35m• Surprise Event: {surprise['text']}\033[0m")

        # Apply main choice effect and daily decay
        player.apply_effects(**effect)
        player.daily_decay()

        # Log event
        event_log_update(current_day, scenario, player_choice, log_choice_text, effect)
        
        # Check survival
        if not player.is_alive():
            print("You have perished... Game Over!")
            player.cause_of_death = "Injury"
            break
        if player.is_food_low(diff_conf["low_food_death_days"]):
            print("Your party was starving for too long... Game Over!")
            player.cause_of_death = "Starvation"
            break
        if player.is_morale_low(diff_conf["low_morale_death_days"]):
            print("Your party got depressed and disbanded... Game Over!")
            player.cause_of_death = "Hopelessness"
            break
        
        print(player.get_stats_as_string())
        
        # End of the day
        print(f"\n===== 🌑 End of day {current_day} 🌑 =====")
        if current_day == NUM_DAYS:
            print("Congratulations! You survived the journey!")
            break
        current_day += 1

    # Printing choices and final score
    print_event_log(final_score(current_day, player.hp, player.food, player.morale, difficulty_mul(player.difficulty)), current_day, player.cause_of_death)

    # Check if player wants to play again
    again = input("\nPlay again? (Y/N): ").strip().upper()
    if again != "Y":
        break