# Swipe Decision Game (Template)

A text-based survival decision game where every day presents you with a choice: swipe left (L) or right (R).  
Your choices affect **Health (HP)**, **Food**, and **Morale**. Survive until the last day to win!

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mistforged/swipe-decision-game.git
   cd SwipeDecisionGame

2. From the project folder run:
   python swipe_decision_game.py

## How to Play

Each day, you face a scenario with two options:
    L → Left choice
    R → Right choice
Some choices have a chance of success/failure, with different effects.
Stats change based on your decisions and surprise events.

## Player Stats

HP – If it reaches 0 → You die.
Food – Decreases daily. If at 0 for too long, you lose HP & morale.
Morale – If low for too long, your party disbands.

## Game Over Conditions

HP reaches 0
Food stays at 0 for too many consecutive days
Morale stays at 0 for too many consecutive days

## Potential Future Improvements
Persistent high score system
More scenarios for variety
Story progression mode

## Author

[Vladimir Jerković](https://github.com/mistforged)