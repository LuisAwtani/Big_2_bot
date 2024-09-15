import random
from collections import defaultdict
from itertools import combinations, product

# Mapping of ranks and suits to numerical values
rankOrder = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5,
             '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
suitOrder = {'D': 0, 'C': 1, 'H': 2, 'S': 3}

# Function to generate a random hand of 13 unique cards
def generateHand():
    ranks = ['3', '4', '5', '6', '7', '8',
             '9', 'T', 'J', 'Q', 'K', 'A', '2']
    suits = ['D', 'C', 'H', 'S']
    deck = [rank + suit for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck[:13]

# Functions to get card values for sorting
def cardValueByRank(card):
    rank, suit = card[0], card[1]
    return (rankOrder[rank], suitOrder[suit])

def cardValueBySuit(card):
    rank, suit = card[0], card[1]
    return (suitOrder[suit], rankOrder[rank])

# Function to find pairs in a hand
def findPairs(hand):
    pairs = []
    rank_dict = defaultdict(list)
    for card in hand:
        rank_dict[card[0]].append(card)
    for cards in rank_dict.values():
        if len(cards) >= 2:
            for pair in combinations(cards, 2):
                pairs.append(list(pair))
    return pairs

# Function to find triples in a hand
def findTriples(hand):
    triples = []
    rank_dict = defaultdict(list)
    for card in hand:
        rank_dict[card[0]].append(card)
    for cards in rank_dict.values():
        if len(cards) >= 3:
            for triple in combinations(cards, 3):
                triples.append(list(triple))
    return triples

# Function to find full houses in a hand
def findFullHouses(hand):
    fullHouses = []
    rank_dict = defaultdict(list)
    for card in hand:
        rank_dict[card[0]].append(card)
    triple_ranks = [rank for rank, cards in rank_dict.items() if len(cards) >= 3]
    pair_ranks = [rank for rank, cards in rank_dict.items() if len(cards) >= 2]
    for triple_rank in triple_ranks:
        triples = list(combinations(rank_dict[triple_rank], 3))
        for triple in triples:
            for pair_rank in pair_ranks:
                if pair_rank != triple_rank:
                    pairs = list(combinations(rank_dict[pair_rank], 2))
                    for pair in pairs:
                        fullHouses.append(list(triple) + list(pair))
    return fullHouses

# Function to find four of a kinds in a hand
def findFourOfAKinds(hand):
    fourOfAKinds = []
    rank_dict = defaultdict(list)
    for card in hand:
        rank_dict[card[0]].append(card)
    for rank, cards in rank_dict.items():
        if len(cards) >= 4:
            quads = list(combinations(cards, 4))
            remaining_cards = [c for c in hand if c[0] != rank]
            for quad in quads:
                for kicker in remaining_cards:
                    fourOfAKinds.append(list(quad) + [kicker])
    return fourOfAKinds

# Function to find straights in a hand
def findStraights(hand):
    straights = []
    rank_dict = defaultdict(list)
    for card in hand:
        rank_value = rankOrder[card[0]]
        rank_dict[rank_value].append(card)
    rank_values = sorted(rank_dict.keys())
    for i in range(len(rank_values) - 4):
        consecutive_ranks = rank_values[i:i+5]
        if consecutive_ranks == list(range(consecutive_ranks[0], consecutive_ranks[0]+5)):
            cards_options = [rank_dict[rank] for rank in consecutive_ranks]
            for combo in product(*cards_options):
                suits = set(card[1] for card in combo)
                if len(suits) >= 2:
                    straights.append(list(combo))
    return straights

# Function to find flushes in a hand
def findFlushes(hand):
    flushes = []
    suit_dict = defaultdict(list)
    for card in hand:
        suit_dict[card[1]].append(card)
    for cards in suit_dict.values():
        if len(cards) >= 5:
            for flush in combinations(cards, 5):
                rank_values = sorted(rankOrder[card[0]] for card in flush)
                if rank_values != list(range(rank_values[0], rank_values[0]+5)):
                    flushes.append(list(flush))
    return flushes

# Function to find straight flushes in a hand
def findStraightFlushes(hand):
    straightFlushes = []
    suit_dict = defaultdict(list)
    for card in hand:
        rank_value = rankOrder[card[0]]
        suit_dict[card[1]].append((rank_value, card))
    for suit, cards in suit_dict.items():
        rank_values = sorted(set(rank_value for rank_value, card in cards))
        rank_to_card = defaultdict(list)
        for rank_value, card in cards:
            rank_to_card[rank_value].append(card)
        for i in range(len(rank_values) - 4):
            consecutive_ranks = rank_values[i:i+5]
            if consecutive_ranks == list(range(consecutive_ranks[0], consecutive_ranks[0]+5)):
                cards_options = [rank_to_card[rank] for rank in consecutive_ranks]
                for combo in product(*cards_options):
                    straightFlushes.append(list(combo))
    return straightFlushes

# Main function
def main():
    print("Press enter to generate a hand:")
    input()
    hand = generateHand()
    print(hand, "\n")

    print("Press enter to sort the hand by rank:")
    input()
    sortedHandByRank = sorted(hand, key=cardValueByRank)
    print(sortedHandByRank, "\n")

    print("Press enter to sort the hand by suit:")
    input()
    sortedHandBySuit = sorted(hand, key=cardValueBySuit)
    print(sortedHandBySuit, "\n")

    hand = sortedHandByRank

    print("Press enter to find singles:")
    input()
    singles = hand  # All cards are singles
    print(singles, "\n")

    print("Press enter to find pairs:")
    input()
    pairs = findPairs(hand)
    print(pairs, "\n")

    print("Press enter to find triples:")
    input()
    triples = findTriples(hand)
    print(triples, "\n")

    print("Press enter to find straights:")
    input()
    straights = findStraights(hand)
    print(straights, "\n")

    print("Press enter to find flushes:")
    input()
    flushes = findFlushes(hand)
    print(flushes, "\n")

    print("Press enter to find full houses:")
    input()
    fullHouses = findFullHouses(hand)
    print(fullHouses, "\n")

    print("Press enter to find four of a kinds:")
    input()
    fourOfAKinds = findFourOfAKinds(hand)
    print(fourOfAKinds, "\n")

    print("Press enter to find straight flushes:")
    input()
    straightFlushes = findStraightFlushes(hand)
    print(straightFlushes, "\n")

if __name__ == "__main__":
    main()