from math import factorial
from collections import defaultdict
from itertools import combinations, product

rankOrder = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5,
             '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}

def S(Card: str):
    ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
    suits = ['S', 'H', 'C', 'D']
    rating = ranks.index(Card[0]) * 4 + suits.index(Card[1])
    return rating

def PossibleArrangements(x: int, y: int):
    return factorial(x) // (factorial(x-y) * factorial(y))

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

# Function that counts number of stronger 5 card tricks that the player DIDN'T HAVE including card x
def DisproverFives(cardsPLayed: list[str], CardsInPLayFunc: list[str]):
    DisproofCounter = 0
    
    # Disprove Flushes
    CardsInPLayFunc = CardsInPLayFunc + cardsPLayed
    NoOfCardsInPlay = len(CardsInPLayFunc)
    
    print(CardsInPLayFunc)
    LastFewIndeces = [(NoOfCardsInPlay -1 - i) for i in range(len(cardsPLayed))]
    #print(f"Last few indices are: {LastFewIndeces}")

    for i in range(NoOfCardsInPlay):
        for j in range(i+1, NoOfCardsInPlay):
            for k in range(j+1, NoOfCardsInPlay):
                for l in range(k+1, NoOfCardsInPlay):
                    for m in range(l+1, NoOfCardsInPlay):
                        #print(f"Checking case: {[CardsInPLayFunc[i], CardsInPLayFunc[j], CardsInPLayFunc[k], CardsInPLayFunc[l], CardsInPLayFunc[m]]}")
                        # Disprove Flushes
                        if CardsInPLayFunc[i][1] == CardsInPLayFunc[m][1] and CardsInPLayFunc[i][1] == CardsInPLayFunc[j][1] and CardsInPLayFunc[i][1] == CardsInPLayFunc[k][1] and CardsInPLayFunc[i][1] == CardsInPLayFunc[l][1]:
                            if i in LastFewIndeces or j in LastFewIndeces or k in LastFewIndeces or l in LastFewIndeces or m in LastFewIndeces:
                                DisproofCounter += 1
                                print(f"Disproved 1 FLush! If Player held {[CardsInPLayFunc[i], CardsInPLayFunc[j], CardsInPLayFunc[k], CardsInPLayFunc[l], CardsInPLayFunc[m]]}")
    return DisproofCounter


x = 13
y = 6
justPlayed = ['9C']
CardsInPlay = ['2C', 'QC', 'TH', '8H', '8C', '8D', '7H', '7C', '7D', '4C', '5D', '4S', '4D']
simplifiedCardsInPlay = ['2C', 'QC', '8C', '7C']
#print(f" Number of cards in play is {len(CardsInPlay)}")
ScardsInGame = [S(x) for x in CardsInPlay]

prb1 = PossibleArrangements(x, y)
prb2 = PossibleArrangements(x-1, y-1)
#print(prb1)
#print(prb2)
#print(y / x)
prb2 = prb2 - 10
#print(prb2 / prb1)
DisproverFives(justPlayed, CardsInPlay)