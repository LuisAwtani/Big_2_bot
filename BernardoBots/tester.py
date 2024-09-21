from math import factorial
from itertools import combinations
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

def is_flush(hand):
    # Helper function to check if a hand is a flush (5 or more cards of the same suit)
    suits = [card[1] for card in hand]  # Extract the suits from the cards
    for suit in set(suits):
        if suits.count(suit) >= 5:
            return True
    return False

def is_straight(hand):
    """Helper function to check if a hand is a straight (5 or more consecutive cards)."""
    # Extract the ranks from the cards, convert them to indices in rank_order
    hand_ranks = sorted([rank_order.index(card[:-1]) for card in hand])
    
    # Check for 5 consecutive ranks (normal and wrapping)
    for i in range(len(hand_ranks) - 4):
        # Check normal straight
        if hand_ranks[i:i+5] == list(range(hand_ranks[i], hand_ranks[i]+5)):
            return True
        # Check wrap-around straight (A-2-3)
        if hand_ranks[-5:] == [0, 1, 2, 11, 12]:  # 3-4-5-A-2 as a special case
            return True
    return False



def disprovenHands(cards, handSize):
    all_hands = list(combinations(cards, handSize))  # Generate all handSize-card hands
    HandsThatWereDisproven = []
    HandsThatWereDisproven.extend([list(hand) for hand in all_hands if is_flush(hand)])  # Filter out hands that form a flush
    HandsThatWereDisproven.extend([list(hand) for hand in all_hands if is_flush(hand)])
    sorted_disproven_hands = [sorted(hand, key=S) for hand in HandsThatWereDisproven]
    return sorted_disproven_hands


def PossibleArrangements(x: int, y: int):
    return factorial(x) // (factorial(x-y) * factorial(y))


# Function estimates probability of PLAYER x holding CARD y for all cards in the game
def DistributionMaker(PlayerHandSize: int, cardsInGame: list, playerNum: int):
    probabilities = []
    #ScardsInGame = [x for x in range(52) if x not in SnotConsidered]
    #cardsInGame = [inverseS(x) for x in ScardsInGame]

    PoolSize = len(cardsInGame)
    TotalPossibleArrangements = PossibleArrangements(PoolSize, PlayerHandSize)
    ArrangementsIncludingCardX = PossibleArrangements(PoolSize - 1, PlayerHandSize - 1)
    CounterOfDisprovenCards = [0 for _ in range(52)]

    DisprovenHands = disprovenHands(cardsInGame, PlayerHandSize)
    print(f"Found {len(DisprovenHands)} hands that were disproven!")

    for flush in DisprovenHands:
        for card in flush:
            CounterOfDisprovenCards[S(card)] += 1
    
    TotalPossibleArrangements -= len(DisprovenHands)
    for Scard in range(52):
        if inverseS(Scard) in cardsInGame:
            DisprovenScenariosWithCardX = CounterOfDisprovenCards[Scard]
            probabilities.append((playerNum, inverseS(Scard), (ArrangementsIncludingCardX - DisprovenScenariosWithCardX)/ TotalPossibleArrangements))
    return probabilities


# y is size of player's hand
playerHandSize = 5

# 8 Cards in play
CardsInPlay = ['2C', 'QC', '3C', '8H', '8C', '2S', '7C', '4C']
#CardsInPlay = ['2C', 'QC', '8H', '8C', '7H', '7C', '4C']

prb1 = PossibleArrangements(len(CardsInPlay), playerHandSize)
prb2 = PossibleArrangements(len(CardsInPlay)-1, playerHandSize-1) 
print(f"Total possible combinations that the player could hold: {prb1}")
print(f"Total possible combinations that include card X: {prb2}")

# Assumed player does not have any hands containing the flush
distribution = DistributionMaker(playerHandSize, CardsInPlay, 1)
print(distribution)

