from collections import defaultdict
from itertools import combinations, product

combinationOrder = {'single': 0, 'pair': 1, 'triple': 2, 'straight': 3, 'flush': 4, 'full house': 5, 'four-of-a-kind': 6, 'straight flush': 7}
rankOrder = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
suitOrder = {'?': 0, 'D': 1, 'C': 2, 'H': 3, 'S': 4}

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


def compareFlushes(flush1, flush2):
    for i in range(4, -1, -1):
        if rankOrder[flush1[i][0]] > rankOrder[flush2[i][0]]:
            return 1
        elif rankOrder[flush1[i][0]] < rankOrder[flush2[i][0]]:
            return 0
    if suitOrder[flush1[0][1]] > suitOrder[flush2[0][1]]:
        return 1
    else:
        return 0


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
        combinations.append([1, 'single', card[0], card[1], [card]])
    for pair in pairs:
        combinations.append([2, 'pair', pair[1][0], pair[1][1], pair])
    for triple in triples:
        combinations.append([3, 'triple', triple[0][0], '?', triple])
    for straight in straights:
        combinations.append([5, 'straight', straight[4][0], straight[4][1], straight])
    for flush in flushes:
        combinations.append([5, 'flush', flush[4][0], flush[4][1], flush])
    for fullHouse in fullHouses:
        combinations.append([5, 'full house', fullHouse[2][0], '?', fullHouse])
    for fourOfAKind in fourOfAKinds:
        combinations.append([5, 'four-of-a-kind', fourOfAKind[2][0], '?', fourOfAKind])
    for straightFlush in straightFlushes:
        combinations.append([5, 'straight flush', straightFlush[4][0], straightFlush[4][1], straightFlush]) 
    return combinations



myHand = ['3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD', '2D']
allCombinations = getAllCombinations(myHand)
# print(allCombinations)
print(len(allCombinations))