# Battle of the Bots: Mystic


## Overview

Welcome to the README for Mystic, a participant in the Battle of the Bots competition. This bot has been designed to compete in the algorithm-based challenges of the Big 2 hackathon hosted by Jane Street. Mystic uses a strategic approach to evaluate hand strengths, calculate optimal plays, and make decisions during gameplay based on the current game state.

## Features

- Card Strength Evaluation: Mystic evaluates the strength of cards in hand using custom metrics that consider card rank and suit, allowing it to make informed decisions.
- Pair Detection: Mystic can identify and play pairs efficiently, improving its chances to beat the opponent’s tricks.
- Trick Strategy: Mystic intelligently selects which tricks to play (single cards, pairs) depending on the cards in its hand and the state of the game.
- Adaptive Play: Based on the cards already played in the match, Mystic dynamically adjusts its strategy, considering the cards left in play (dead cards).

## Setup

1. **Requirements**:
   - Python version: 3.8 or higher
   - Dependencies:
   - classes.py (the folder provided by competition hosts)


2. **Installation**:
   - Clone this repository:
     ```bash
     git clone https://github.com/yourusername/mystic.git
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## Usage

1. **Running the Bot**:
   - Execute the bot using the following command:
     ```bash
     python Mystic.py
     ```

2. **Configuration**:
   - Game State: The bot operates based on game state passed to it in the form of a MatchState object, which provides data on the current match, your hand, and the cards you need to beat.
   - Hand Input: The bot requires hand input in the form of a sorted list of card strengths (denoted as S values), not card strings.

## Testing

- To test Mystic, you can run it within a local Big 2 simulation, where the game state is set up and passed to the bot. Ensure that MatchState and GameHistory objects are properly populated.
- Example of running tests using pytest (if you have test cases written):
bash
Copy code


## Log Files

- : The bot generates log files for each match, detailing the actions and outcomes. Review these files to debug and refine your strategy. Ensure you download any log files you need as our server only retains the most recent 20 logs per team.



## Contact

- For questions or support regarding this bot, please contact me luisbernardo.a23@gmail.com.

---
