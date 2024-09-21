from math import factorial
from collections import defaultdict
from itertools import combinations, product
rank_order = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
suit_order = {'D': 0, 'C': 1, 'H': 2, 'S': 3}


def S(Card: str):
    ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
    suits = ['S', 'H', 'C', 'D']
    rating = ranks.index(Card[0]) * 4 + suits.index(Card[1])
    return rating

def inverseS(rating: int):
    ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
    suits = ['S', 'H', 'C', 'D']
    index = rating // 4
    suitIndex = rating % 4
    return ranks[index] + suits[suitIndex]

def PossibleArrangements(x: int, y: int):
    return factorial(x) // (factorial(x-y) * factorial(y))

# Helper functions to check various trick types
def is_flush(hand):
    suits = [card[1] for card in hand]
    return len(set(suits)) == 1

def is_straight(hand):
    hand_ranks = sorted([rank_order.index(card[0]) for card in hand])
    for i in range(len(hand_ranks) - 4):
        if hand_ranks[i:i+5] == list(range(hand_ranks[i], hand_ranks[i]+5)):
            return True
    return False

def is_full_house(hand):
    rank_count = {}
    for card in hand:
        rank = card[0]
        rank_count[rank] = rank_count.get(rank, 0) + 1
    return 3 in rank_count.values() and 2 in rank_count.values()

def is_four_of_a_kind(hand):
    rank_count = {}
    for card in hand:
        rank = card[0]
        rank_count[rank] = rank_count.get(rank, 0) + 1
    return 4 in rank_count.values()

def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)

def strongest_card(hand):
    """Finds the strongest card in a hand based on the S value."""
    return min(hand, key=S)

def compare_hands(hand1, hand2):
    """
    Compare two hands based on their strongest cards using the S function.
    Returns True if hand1 is weaker than hand2 (i.e., has higher S value), False otherwise.
    """
    return S(strongest_card(hand1)) < S(strongest_card(hand2))

def disprovenHands(cards, trick_type, strongest_card_of_trick, hand_size, playerNum):
    """
    Outputs a list of lists, where each sublist is a hand we've disproven
    (i.e., hands that form a flush, straight, full house, straight flush, or four of a kind),
    with the strongest card at the 0th index.
    
    Parameters:
    cards (list): The remaining cards among other players.
    trick_type (str): The type of 5-card trick being compared (flush, straight, full house, etc.).
    strongest_card_of_trick (str): The strongest card of the already played trick.
    hand_size (int): The number of cards the player holds.
    
    Returns:
    list: A list of hands (disproven hands) that form the same or stronger type of trick but are weaker than the input trick.
    """
    all_k_card_combinations = list(combinations(cards, hand_size))  # Generate all hand_size-card combinations
    disproven_hands = []
    
    # Iterate through all possible k-card hands
    for hand in all_k_card_combinations:
        hand = list(hand)
        valid_5_card_tricks = []

        # Evaluate all 5-card subsets of this k-sized hand
        for five_card_subset in combinations(hand, 5):
            five_card_subset = list(five_card_subset)

            # Handle each trick type in descending strength order
            if trick_type == 'straight flush' and is_straight_flush(five_card_subset):
                if compare_hands(five_card_subset, [strongest_card_of_trick]):
                    valid_5_card_tricks.append(five_card_subset)
            elif trick_type == 'four of a kind':
                if is_four_of_a_kind(five_card_subset):
                    if compare_hands(five_card_subset, [strongest_card_of_trick]):
                        valid_5_card_tricks.append(five_card_subset)
                elif is_straight_flush(five_card_subset):  # Stronger than four of a kind, automatically add
                    valid_5_card_tricks.append(five_card_subset)
            elif trick_type == 'full house':
                if is_full_house(five_card_subset):
                    if compare_hands(five_card_subset, [strongest_card_of_trick]):
                        valid_5_card_tricks.append(five_card_subset)
                elif is_four_of_a_kind(five_card_subset) or is_straight_flush(five_card_subset):
                    valid_5_card_tricks.append(five_card_subset)
            elif trick_type == 'flush':
                if is_flush(five_card_subset):
                    if compare_hands(five_card_subset, [strongest_card_of_trick]):
                        valid_5_card_tricks.append(five_card_subset)
                elif is_full_house(five_card_subset) or is_four_of_a_kind(five_card_subset) or is_straight_flush(five_card_subset):
                    valid_5_card_tricks.append(five_card_subset)
            elif trick_type == 'straight':
                if is_straight(five_card_subset):
                    if compare_hands(five_card_subset, [strongest_card_of_trick]):
                        valid_5_card_tricks.append(five_card_subset)
                elif is_flush(five_card_subset) or is_full_house(five_card_subset) or is_four_of_a_kind(five_card_subset) or is_straight_flush(five_card_subset):
                    valid_5_card_tricks.append(five_card_subset)

        # If valid tricks were found, add the k-sized hand
        if valid_5_card_tricks:
            strongest_trick = min(valid_5_card_tricks, key=lambda hand: S(strongest_card(hand)))  # Pick strongest 5-card trick
            hand_sorted = sorted(hand, key=S)  # Sort entire k-sized hand by strength (S value)
            disproven_hands.append(hand_sorted)

    table = tableGenerator(playerNum, disproven_hands, cards, hand_size)
    return table


def tableGenerator(playerNum: int, disprovenHands: list, cardsInPlay: list, playerHandSize):
    prb1 = PossibleArrangements(len(cardsInPlay), playerHandSize)
    prb2 = PossibleArrangements(len(cardsInPlay)-1, playerHandSize-1) 
    totalDisprovenScenarios = len(disprovenHands)
    table = []
    disprovenList = [0 for _ in range(52)]
    for hand in disprovenHands:
        for card in hand:
            disprovenList[S(card)] += 1

    for card in cardsInPlay:
        table.append((playerNum, card, (prb2 - disprovenList[S(card)]) / (prb1 - totalDisprovenScenarios)))

    return table


#CardsInPlay = ['2C', 'QC', '3C', '8H', '8C', '2S', '7C', 'TC', 'AS', '3H', '5C', 'JS', '4C']  # Remaining cards
CardsInPlay = ['2C', 'QC', '3C', '8C', '7C', 'AS', '3H', 'TC', '2S', '5C', '8H', 'JS', 'QS']
handSize = 5  # Player's hand size
trick_type = 'flush'  # Trick type to compare
strongest_card_of_trick = 'TD'  # Strongest card in the already played trick
disproven = disprovenHands(CardsInPlay, trick_type, strongest_card_of_trick, handSize, 1)
print(disproven)

