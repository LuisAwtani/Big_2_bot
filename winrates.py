import os
import glob
import re
from collections import defaultdict

def assign_ranks(sorted_list):
    ranks = {}
    rank = 1
    prev_points = None
    count = 1  # Number of players sharing the same rank
    for i, (player_name, points) in enumerate(sorted_list):
        if i == 0:
            rank = 1
        else:
            if points == prev_points:
                # Rank remains the same for tied scores
                count += 1
            else:
                rank += count
                count = 1
        ranks[player_name] = rank
        prev_points = points
    return ranks

def main():
    # Path to the Downloads folder
    download_folder = os.path.expanduser('~/Downloads')
    # Get all .txt files in the Downloads folder
    log_files = glob.glob(os.path.join(download_folder, '*.txt'))

    # Dictionaries to store the results
    mystic_vs = defaultdict(lambda: [0, 0, 0])  # {player_name: [wins, losses, ties]}
    overall_wins = defaultdict(int)
    player_matches = defaultdict(set)  # {player_name: set of log files}
    player_ranks = defaultdict(list)  # {player_name: list of ranks}

    # Regex patterns to match the required lines
    player_result_pattern = re.compile(
        r'Engine: (?P<player_name>.+?) finished with (?P<cards_in_hand>\d+) cards in hand\. They are now on (?P<points>-?\d+) points'
    )
    overall_winner_pattern = re.compile(
        r'Engine: Overall winner is (?P<player_name>.+?) with a score of (?P<score>-?\d+)\.'
    )

    for log_file in log_files:
        players_in_match = set()
        cumulative_points = {}  # {player_name: final_cumulative_points}
        with open(log_file, 'r') as f:
            current_game = []
            for line in f:
                line = line.strip()
                # Match player result lines
                player_match = player_result_pattern.match(line)
                if player_match:
                    player_name = player_match.group('player_name')
                    cards_in_hand = int(player_match.group('cards_in_hand'))
                    points = int(player_match.group('points'))
                    players_in_match.add(player_name)
                    cumulative_points[player_name] = points  # Update cumulative points
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

        # Assign ranks based on cumulative points
        sorted_players = sorted(cumulative_points.items(), key=lambda x: x[1], reverse=True)
        ranks = assign_ranks(sorted_players)

        # Update player_ranks with the ranks from this match
        for player_name, rank in ranks.items():
            player_ranks[player_name].append(rank)

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

    # Output the overall wins, matches played, and average rank of each player
    print("\nOverall wins, matches played, and average rank of each player:")

    # Create a list to store (player, overall_win_count, matches_played, average_rank)
    player_data = []

    # Get all players from the player_matches dictionary
    all_players = set(player_matches.keys())

    # Loop through each player to calculate stats
    for player in all_players:
        matches_played = len(player_matches[player])
        overall_win_count = overall_wins.get(player, 0)
        average_rank = sum(player_ranks[player]) / len(player_ranks[player])
        overall_win_rate = overall_win_count / matches_played if matches_played > 0 else 0
        # Append the player's data to the list
        player_data.append((player, overall_win_count, matches_played, average_rank))

    # Sort the list by average rank in increasing order (ascending)
    player_data.sort(key=lambda x: x[3])  # x[3] is the average_rank

    # Print the sorted data
    for player, overall_win_count, matches_played, average_rank in player_data:
        print(f"{player}: {overall_win_count} overall wins, appeared in {matches_played} matches, average rank: {average_rank:.2f}")

if __name__ == "__main__":
    main()