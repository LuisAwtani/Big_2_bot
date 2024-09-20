from classes import *
from collections import defaultdict
from itertools import combinations, product

class Algorithm:
    combinationOrder = {'single': 0, 'pair': 1, 'triple': 2, 'straight': 3, 'flush': 4, 'full house': 5, 'four-of-a-kind': 6, 'straight flush': 7}
    rankOrder = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
    suitOrder = {'D': 0, 'C': 1, 'H': 2, 'S': 3}


    @staticmethod
    def sortCards(cards): # returns a list of cards sorted by rank and suit
        return sorted(cards, key=lambda card: (Algorithm.rankOrder.get(card[0], 99), Algorithm.suitOrder.get(card[1], 99)))


    @staticmethod
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


    @staticmethod
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
    

    @staticmethod
    def findStraights(hand):
        straights = []
        rankDict = defaultdict(list)
        for card in hand:
            rankValue = Algorithm.rankOrder[card[0]]
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
    

    @staticmethod
    def findFlushes(hand):
        flushes = []
        suitDict = defaultdict(list)
        for card in hand:
            suitDict[card[1]].append(card)
        for cards in suitDict.values():
            if len(cards) >= 5:
                for flush in combinations(cards, 5):
                    rankValues = sorted(Algorithm.rankOrder[card[0]] for card in flush)
                    if rankValues != list(range(rankValues[0], rankValues[0]+5)):
                        flushes.append(list(flush))
        return flushes


    @staticmethod
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
    

    @staticmethod
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


    @staticmethod
    def findStraightFlushes(hand):
        straightFlushes = []
        suitDict = defaultdict(list)
        for card in hand:
            rankValue = Algorithm.rankOrder[card[0]]
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


    @staticmethod
    def getCurrentTrickType(trick: Trick): # returns [type, rank to beat, (suit to beat)]
        if trick is None:
            return ['start']
        else:
            trick = Algorithm.sortCards(trick.cards)
            if len(trick) == 5:
                if trick[0][1] == trick[1][1] == trick[2][1] == trick[3][1] == trick[4][1]:
                    if Algorithm.rankOrder[trick[0][0]] == Algorithm.rankOrder[trick[1][0]] - 1 == Algorithm.rankOrder[trick[2][0]] - 2 == Algorithm.rankOrder[trick[3][0]] - 3 == Algorithm.rankOrder[trick[4][0]] - 4:
                        return ['straight flush', trick[4][0], trick[4][1]] # type, rank to beat, suit to beat
                    else:
                        return ['flush', trick[4][0], trick[4][1]] # type, rank to beat, suit to beat
                elif Algorithm.rankOrder[trick[0][0]] == Algorithm.rankOrder[trick[1][0]] - 1 == Algorithm.rankOrder[trick[2][0]] - 2 == Algorithm.rankOrder[trick[3][0]] - 3 == Algorithm.rankOrder[trick[4][0]] - 4:
                    return ['straight', trick[4][0], trick[4][1]] # type, rank to beat, suit to beat
                elif trick[1][0] == trick[2][0] == trick[3][0]:
                    return ['four-of-a-kind', trick[2][0]] # type, rank to beat
                else:
                    return ['full house', trick[2][0]] # type, rank to beat
            elif len(trick) == 3:
                return ['triple', trick[0][0]] # type, rank to beat
            elif len(trick) == 2:
                return ['pair', trick[1][0], trick[1][1]] # type, rank to beat, suit to beat
            else:
                return ['single', trick[0][0], trick[0][1]] # type, rank to beat, suit to beat


    @staticmethod
    def getAllCombinations(hand): # returns [[type, rank, (suit), [cards]]]
        combinations = []
        pairs = Algorithm.findPairs(hand)
        triples = Algorithm.findTriples(hand)
        straights = Algorithm.findStraights(hand)
        flushes = Algorithm.findFlushes(hand)
        fullHouses = Algorithm.findFullHouses(hand)
        fourOfAKinds = Algorithm.findFourOfAKinds(hand)
        straightFlushes = Algorithm.findStraightFlushes(hand)
        for card in hand:
            combinations.append(['single', card[0], card[1], [card]]) # type, rank, suit, cards
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


    def getAction(Algorithm, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration

        # TODO Write your algorithm logic here

        print("DUM-E V3 MODEL")

        myHand = state.myHand
        myHand = Algorithm.sortCards(myHand)
        # print("MY HAND")
        # print(myHand)

        toBeat = state.toBeat
        currentTrick = Algorithm.getCurrentTrickType(toBeat)
        # print("CURRENT TRICK")
        # print(currentTrick)
        
        allCombinations = Algorithm.getAllCombinations(myHand)
        # print("ALL COMBINATIONS")
        # print(allCombinations)

        if currentTrick[0] == 'start':
            action = allCombinations[0][3]

        elif currentTrick[0] == 'single':
            for combination in allCombinations:
                if combination[0] == 'single':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break
                    elif Algorithm.rankOrder[combination[1]] == Algorithm.rankOrder[currentTrick[1]]:
                        if Algorithm.suitOrder[combination[2]] > Algorithm.suitOrder[currentTrick[2]]:
                            action = combination[3]
                            break

        elif currentTrick[0] == 'pair':
            for combination in allCombinations:
                if combination[0] == 'pair':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break
                    elif Algorithm.rankOrder[combination[1]] == Algorithm.rankOrder[currentTrick[1]]:
                        if Algorithm.suitOrder[combination[2]] > Algorithm.suitOrder[currentTrick[2]]:
                            action = combination[3]
                            break
                            
        elif currentTrick[0] == 'triple':
            for combination in allCombinations:
                if combination[0] == 'triple':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break

        elif currentTrick[0] == 'straight':
            for combination in allCombinations:
                if combination[0] == 'straight':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break
                    elif Algorithm.rankOrder[combination[1]] == Algorithm.rankOrder[currentTrick[1]]:
                        if Algorithm.suitOrder[combination[2]] > Algorithm.suitOrder[currentTrick[2]]:
                            action = combination[3]
                            break
                elif Algorithm.combinationOrder[combination[0]] > Algorithm.combinationOrder[currentTrick[0]]:
                    action = combination[3]
                    break

        elif currentTrick[0] == 'flush':
            for combination in allCombinations:
                if combination[0] == 'flush':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break
                    elif Algorithm.rankOrder[combination[1]] == Algorithm.rankOrder[currentTrick[1]]:
                        if Algorithm.suitOrder[combination[2]] > Algorithm.suitOrder[currentTrick[2]]:
                            action = combination[3]
                            break
                elif Algorithm.combinationOrder[combination[0]] > Algorithm.combinationOrder[currentTrick[0]]:
                    action = combination[3]
                    break
        
        elif currentTrick[0] == 'full house':
            for combination in allCombinations:
                if combination[0] == 'full house':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break
                elif Algorithm.combinationOrder[combination[0]] > Algorithm.combinationOrder[currentTrick[0]]:
                    action = combination[3]
                    break

        elif currentTrick[0] == 'four-of-a-kind':
            for combination in allCombinations:
                if combination[0] == 'four-of-a-kind':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break
                elif Algorithm.combinationOrder[combination[0]] > Algorithm.combinationOrder[currentTrick[0]]:
                    action = combination[3]
                    break

        elif currentTrick[0] == 'straight flush':
            for combination in allCombinations:
                if combination[0] == 'straight flush':
                    if Algorithm.rankOrder[combination[1]] > Algorithm.rankOrder[currentTrick[1]]:
                        action = combination[3]
                        break
                    elif Algorithm.rankOrder[combination[1]] == Algorithm.rankOrder[currentTrick[1]]:
                        if Algorithm.suitOrder[combination[2]] > Algorithm.suitOrder[currentTrick[2]]:
                            action = combination[3]
                            break
                elif Algorithm.combinationOrder[combination[0]] > Algorithm.combinationOrder[currentTrick[0]]:
                    action = combination[3]
                    break

        return action, myData