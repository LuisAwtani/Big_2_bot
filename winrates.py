import os
import glob
import re
from collections import defaultdict

def main():
    # Path to the Downloads folder
    download_folder = os.path.expanduser('~/Downloads')
    # Get all .txt files in the Downloads folder
    log_files = glob.glob(os.path.join(download_folder, '*.txt'))

    # Dictionaries to store the results
    mystic_vs = defaultdict(lambda: [0, 0, 0])  # {player_name: [wins, losses, ties]}
    overall_wins = defaultdict(int)
    player_matches = defaultdict(set)  # {player_name: set of log files}

    # Regex patterns to match the required lines
    player_result_pattern = re.compile(
        r'Engine: (?P<player_name>.+?) finished with (?P<cards_in_hand>\d+) cards in hand\. They are now on (?P<points>-?\d+) points'
    )
    overall_winner_pattern = re.compile(
        r'Engine: Overall winner is (?P<player_name>.+?) with a score of (?P<score>-?\d+)\.'
    )

    for log_file in log_files:
        players_in_match = set()
        with open(log_file, 'r') as f:
            current_game = []
            for line in f:
                line = line.strip()
                # Match player result lines
                player_match = player_result_pattern.match(line)
                if player_match:
                    player_name = player_match.group('player_name')
                    cards_in_hand = int(player_match.group('cards_in_hand'))
                    players_in_match.add(player_name)
                    current_game.append((player_name, cards_in_hand))
                    if len(current_game) == 4:
                        # Process the game results
                        mystic_cards = None
                        for player in current_game:
                            if player[0] == 'Mystic':
                                mystic_cards = player[1]
                                break
                        if mystic_cards is not None:
                            for player in current_game:
                                if player[0] != 'Mystic':
                                    other_player = player[0]
                                    other_cards = player[1]
                                    if mystic_cards < other_cards:
                                        mystic_vs[other_player][0] += 1  # Win
                                    elif mystic_cards > other_cards:
                                        mystic_vs[other_player][1] += 1  # Loss
                                    else:
                                        mystic_vs[other_player][2] += 1  # Tie
                        current_game = []
                else:
                    # Match the overall winner line
                    overall_match = overall_winner_pattern.match(line)
                    if overall_match:
                        winner_name = overall_match.group('player_name')
                        overall_wins[winner_name] += 1
                        players_in_match.add(winner_name)

        # Update player_matches with the players in this match
        for player_name in players_in_match:
            player_matches[player_name].add(log_file)

    # Output Mystic's win rate against each player
    print("Mystic's win rate against each player based on cards in hand:")
    # Create a list of tuples with player and win rate
    win_rate_list = []

    # Calculate win rate for each player
    for player, record in mystic_vs.items():
        wins, losses, ties = record
        total_games = wins + losses + ties
        win_rate = wins / total_games if total_games > 0 else 0
        win_rate_list.append((player, wins, losses, ties, win_rate))

    # Sort by win rate in increasing order
    win_rate_list.sort(key=lambda x: x[4])  # x[4] is the win rate

    # Output the sorted results
    for player, wins, losses, ties, win_rate in win_rate_list:
        print(f"Against {player}: {wins} wins, {losses} losses, {ties} ties. Win rate: {win_rate:.2%}")

    # Output the overall wins and matches played of each player
    print("\nOverall wins and matches played of each player:")
    for player, count in overall_wins.items():
        matches_played = len(player_matches[player])
        print(f"{player}: {count} overall wins, appeared in {matches_played} matches. Overall win rate: {count / matches_played:.2%}")

    # For players who didn't win overall but appeared in matches
    other_players = set(player_matches.keys()) - set(overall_wins.keys())
    for player in other_players:
        matches_played = len(player_matches[player])
        print(f"{player}: 0 overall wins, appeared in {matches_played} matches. Overall win rate: 0.00%")

if __name__ == "__main__":
    main()