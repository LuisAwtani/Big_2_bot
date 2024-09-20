from classes import *
from collections import defaultdict
from itertools import combinations, product


rankOrder = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
suitOrder = {'D': 0, 'C': 1, 'H': 2, 'S': 3}

    
def sortCards(cards):
    return sorted(cards, key=lambda card: (rankOrder.get(card[0], 99), suitOrder.get(card[1], 99)))


def findPairs(hand):
    pairs = []
    rankDict = defaultdict(list)
    for card in hand:
        rankDict[card[0]].append(card)
    for cards in rankDict.values():
        if len(cards) >= 2:
            for pair in combinations(cards, 2):
                pairs.append(list(pair))
    return pairs


def findTriples(hand):
    triples = []
    rankDict = defaultdict(list)
    for card in hand:
        rankDict[card[0]].append(card)
    for cards in rankDict.values():
        if len(cards) >= 3:
            for triple in combinations(cards, 3):
                triples.append(list(triple))
    return triples


def findStraights(hand):
    straights = []
    rankDict = defaultdict(list)
    for card in hand:
        rankValue = rankOrder[card[0]]
        rankDict[rankValue].append(card)
    rankValues = sorted(rankDict.keys())
    for i in range(len(rankValues) - 4):
        consecutiveRanks = rankValues[i:i+5]
        if consecutiveRanks == list(range(consecutiveRanks[0], consecutiveRanks[0]+5)):
            cardsOptions = [rankDict[rank] for rank in consecutiveRanks]
            for combo in product(*cardsOptions):
                suits = set(card[1] for card in combo)
                if len(suits) >= 2:
                    straights.append(list(combo))
    return straights


def findFlushes(hand):
    flushes = []
    suitDict = defaultdict(list)
    for card in hand:
        suitDict[card[1]].append(card)
    for cards in suitDict.values():
        if len(cards) >= 5:
            for flush in combinations(cards, 5):
                rankValues = sorted(rankOrder[card[0]] for card in flush)
                if rankValues != list(range(rankValues[0], rankValues[0]+5)):
                    flushes.append(list(flush))
    return flushes


def findFullHouses(hand):
    fullHouses = []
    rankDict = defaultdict(list)
    for card in hand:
        rankDict[card[0]].append(card)
    tripleRanks = [rank for rank, cards in rankDict.items() if len(cards) >= 3]
    pairRanks = [rank for rank, cards in rankDict.items() if len(cards) >= 2]
    for tripleRank in tripleRanks:
        triples = list(combinations(rankDict[tripleRank], 3))
        for triple in triples:
            for pairRank in pairRanks:
                if pairRank != tripleRank:
                    pairs = list(combinations(rankDict[pairRank], 2))
                    for pair in pairs:
                        fullHouses.append(list(triple) + list(pair))
    return fullHouses


def findFourOfAKinds(hand):
    fourOfAKinds = []
    rankDict = defaultdict(list)
    for card in hand:
        rankDict[card[0]].append(card)
    for rank, cards in rankDict.items():
        if len(cards) >= 4:
            quads = list(combinations(cards, 4))
            remainingCards = [c for c in hand if c[0] != rank]
            for quad in quads:
                for kicker in remainingCards:
                    fourOfAKinds.append(list(quad) + [kicker])
    return fourOfAKinds


def findStraightFlushes(hand):
    straightFlushes = []
    suitDict = defaultdict(list)
    for card in hand:
        rankValue = rankOrder[card[0]]
        suitDict[card[1]].append((rankValue, card))
    for suit, cards in suitDict.items():
        rankValues = sorted(set(rankValue for rankValue, card in cards))
        rankToCard = defaultdict(list)
        for rankValue, card in cards:
            rankToCard[rankValue].append(card)
        for i in range(len(rankValues) - 4):
            consecutiveRanks = rankValues[i:i+5]
            if consecutiveRanks == list(range(consecutiveRanks[0], consecutiveRanks[0]+5)):
                cardsOptions = [rankToCard[rank] for rank in consecutiveRanks]
                for combo in product(*cardsOptions):
                    straightFlushes.append(list(combo))
    return straightFlushes


def getCurrentTrickType(trick):
    if len(trick) == 5:
        if trick[0][1] == trick[1][1] == trick[2][1] == trick[3][1] == trick[4][1]:
            if rankOrder[trick[0][0]] == rankOrder[trick[1][0]] - 1 == rankOrder[trick[2][0]] - 2 == rankOrder[trick[3][0]] - 3 == rankOrder[trick[4][0]] - 4:
                return ['straight flush', trick[4][0], trick[4][1]] # type, rank to beat, suit to beat
            else:
                return ['flush', trick[4][0], trick[4][1]] # type, rank to beat, suit to beat
        elif rankOrder[trick[0][0]] == rankOrder[trick[1][0]] - 1 == rankOrder[trick[2][0]] - 2 == rankOrder[trick[3][0]] - 3 == rankOrder[trick[4][0]] - 4:
            return ['straight', trick[4][0], trick[4][1]] # type, rank to beat, suit to beat
        elif trick[1][0] == trick[2][0] == trick[3][0]:
            return ['four-of-a-kind', trick[2][0]] # type, rank to beat
        else:
            return ['full house', trick[2][0]] # type, rank to beat
    elif len(trick) == 3:
        return ['triple', trick[0][0]] # type, rank to beat
    elif len(trick) == 2:
        return ['pair', trick[1][0], trick[1][1]] # type, rank to beat, suit to beat
    elif len(trick) == 1:
        return ['single', trick[0][0], trick[0][1]] # type, rank to beat, suit to beat
    else:
        return ['start'] # type


def getAllCombinations(hand):
    combinations = []
    pairs = findPairs(hand)
    triples = findTriples(hand)
    straights = findStraights(hand)
    flushes = findFlushes(hand)
    fullHouses = findFullHouses(hand)
    fourOfAKinds = findFourOfAKinds(hand)
    straightFlushes = findStraightFlushes(hand)
    for card in hand:
        combinations.append(['single', card[0], card[1], card]) # type, rank, suit, cards
    for pair in pairs:
        combinations.append(['pair', pair[1][0], pair[1][1], pair]) # type, rank, suit, cards
    for triple in triples:
        combinations.append(['triple', triple[0][0], triple]) # type, rank, cards
    for straight in straights:
        combinations.append(['straight', straight[4][0], straight[4][1], straight]) # type, rank, suit, cards
    for flush in flushes:
        combinations.append(['flush', flush[4][0], flush[4][1], flush]) # type, rank, suit, cards
    for fullHouse in fullHouses:
        combinations.append(['full house', fullHouse[2][0], fullHouse]) # type, rank, cards
    for fourOfAKind in fourOfAKinds:
        combinations.append(['four-of-a-kind', fourOfAKind[2][0], fourOfAKind]) # type, rank, cards
    for straightFlush in straightFlushes:
        combinations.append(['straight flush', straightFlush[4][0], straightFlush[4][1], straightFlush]) # type, rank, suit, cards
    return combinations


def main():
    myHand = ['3C', 'AD', 'KH', '2H', '6S', '2C', '4D', '6C', '7D', 'JS', 'AH', '6D', '2D']
    myHand = sortCards(myHand)

    print("MY HAND")
    print(myHand)

    allCombinations = getAllCombinations(myHand)
    print("ALL COMBINATIONS")
    print(allCombinations)


if __name__ == "__main__":
    main()