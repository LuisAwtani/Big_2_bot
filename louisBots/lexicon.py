from classes import *
from collections import Counter, defaultdict
from itertools import combinations, product

class Algorithm:
    COMBO_ORDER = {'single': 0, 'pair': 1, 'triple': 2, 'straight': 3, 'flush': 4, 'full house': 5, 'four-of-a-kind': 6, 'straight flush': 7}
    RANK_ORDER = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
    SUIT_ORDER = {'?': 0, 'D': 1, 'C': 2, 'H': 3, 'S': 4}
    SCORING = {
        'straight flush': 50,
        'four-of-a-kind': 45,
        'full house': 40,
        'flush': 35,
        'straight': 30,
        'triple': 20,
        'pair': 15
    }


    @staticmethod
    def sortCards(cards): # returns a list of cards sorted by rank and suit
        return sorted(cards, key=lambda card: (Algorithm.RANK_ORDER.get(card[0], 99), Algorithm.SUIT_ORDER.get(card[1], 99)))


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
            rankValue = Algorithm.RANK_ORDER[card[0]]
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
                    rankValues = sorted(Algorithm.RANK_ORDER[card[0]] for card in flush)
                    if rankValues != list(range(rankValues[0], rankValues[0]+5)):
                        flushes.append(list(flush))
        return flushes


    @staticmethod
    def compareFlushes(flush1, flush2):
        for i in range(4, -1, -1):
            if Algorithm.RANK_ORDER[flush1[i][0]] > Algorithm.RANK_ORDER[flush2[i][0]]:
                return 1
            elif Algorithm.RANK_ORDER[flush1[i][0]] < Algorithm.RANK_ORDER[flush2[i][0]]:
                return 0
        if Algorithm.SUIT_ORDER[flush1[0][1]] > Algorithm.SUIT_ORDER[flush2[0][1]]:
            return 1
        else:
            return 0


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
            rankValue = Algorithm.RANK_ORDER[card[0]]
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
    def getCurrentTrickType(trick: Trick): # returns [type length, type, rank to beat, suit to beat]
        if trick is None:
            return [0, 'start']
        else:
            trick = Algorithm.sortCards(trick.cards)
            if len(trick) == 5:
                if trick[0][1] == trick[1][1] == trick[2][1] == trick[3][1] == trick[4][1]:
                    if Algorithm.RANK_ORDER[trick[0][0]] == Algorithm.RANK_ORDER[trick[1][0]] - 1 == Algorithm.RANK_ORDER[trick[2][0]] - 2 == Algorithm.RANK_ORDER[trick[3][0]] - 3 == Algorithm.RANK_ORDER[trick[4][0]] - 4:
                        return [5, 'straight flush', trick[4][0], trick[4][1]]
                    else:
                        return [5, 'flush', trick[4][0], trick[4][1]]
                elif Algorithm.RANK_ORDER[trick[0][0]] == Algorithm.RANK_ORDER[trick[1][0]] - 1 == Algorithm.RANK_ORDER[trick[2][0]] - 2 == Algorithm.RANK_ORDER[trick[3][0]] - 3 == Algorithm.RANK_ORDER[trick[4][0]] - 4:
                    return [5, 'straight', trick[4][0], trick[4][1]]
                elif trick[1][0] == trick[2][0] == trick[3][0]:
                    return [5, 'four-of-a-kind', trick[2][0], '?']
                else:
                    return [5, 'full house', trick[2][0], '?']
            elif len(trick) == 3:
                return [3, 'triple', trick[0][0], '?']
            elif len(trick) == 2:
                return [2, 'pair', trick[1][0], trick[1][1]]
            else:
                return [1, 'single', trick[0][0], trick[0][1]]


    @staticmethod
    def getAllCombinations(hand): # returns [[type length, type, rank, suit, [cards]]]
        combinations = []
        pairs = Algorithm.findPairs(hand)
        triples = Algorithm.findTriples(hand)
        straights = Algorithm.findStraights(hand)
        flushes = Algorithm.findFlushes(hand)
        fullHouses = Algorithm.findFullHouses(hand)
        fourOfAKinds = Algorithm.findFourOfAKinds(hand)
        straightFlushes = Algorithm.findStraightFlushes(hand)
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


    @staticmethod
    def getAllOrganisations(hand, allCombinations):
        # Step 1: Create card to bit mapping
        cardToBit = {card: 1 << i for i, card in enumerate(hand)}

        # Step 2: Separate singles and multis
        singles = [c for c in allCombinations if c[1] == 'single']
        multis = [c for c in allCombinations if c[1] != 'single']

        # Step 3: Create a mapping from card to single combination for quick lookup
        singleMap = {c[4][0]: c for c in singles}

        organisations = []

        def backtrack(usedBits, currentOrganisation, startIndex):
            # If all cards in the hand are used
            if bin(usedBits).count('1') == len(hand):
                organisations.append(currentOrganisation.copy())
                return

            # If we've considered all multis, try to fill the rest with singles
            if startIndex >= len(multis):
                # Calculate remaining bits (cards not used)
                remaining_bits = 0
                for card, bit in cardToBit.items():
                    remaining_bits |= bit if card not in singleMap else 0
                # Count remaining singles
                remainingCards = [card for card in singleMap if not (usedBits & cardToBit[card])]
                if bin(usedBits | sum([cardToBit[card] for card in remainingCards])).count('1') == len(hand):
                    # Add all remaining singles
                    orgWithSingles = currentOrganisation.copy()
                    for card in remainingCards:
                        orgWithSingles.append(singleMap[card])
                    organisations.append(orgWithSingles)
                return

            for i in range(startIndex, len(multis)):
                multi = multis[i]
                multiBits = 0
                for card in multi[4]:
                    multiBits |= cardToBit[card]

                # Check if multi_bits overlap with used_bits
                if (multiBits & usedBits) == 0:
                    # Choose this multi
                    currentOrganisation.append(multi)
                    usedBits |= multiBits

                    # Recurse with the next combinations
                    backtrack(usedBits, currentOrganisation, i + 1)

                    # Backtrack
                    currentOrganisation.pop()
                    usedBits &= ~multiBits

            # After trying all multis, try to add singles if possible
            remainingCards = [card for card in singleMap if not (usedBits & cardToBit[card])]
            if bin(usedBits | sum([cardToBit[card] for card in remainingCards])).count('1') == len(hand):
                orgWithSingles = currentOrganisation.copy()
                for card in remainingCards:
                    orgWithSingles.append(singleMap[card])
                organisations.append(orgWithSingles)

        # Initialize backtracking with used_bits = 0 (no cards used)
        backtrack(0, [], 0)

        return organisations


    @staticmethod
    def getAllScores(allOrganisations):
        scores = []
        for organisation in allOrganisations:
            score = 0
            for combination in organisation:
                if combination[1] == 'single':
                    if combination[-1][0] == '2S':
                        score += 30
                    elif combination[-1][0][0] == '2':
                        score += 20
                    elif combination[-1][0][0] == 'A':
                        score += 10
                    else:
                        score += 5
                else:
                    score += Algorithm.SCORING[combination[1]]
            scores.append(score)
        return scores


    def getAction(Algorithm, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration

        # TODO Write your algorithm logic here

        print("LEXICON V1 MODEL")

        hand = state.myHand
        hand = Algorithm.sortCards(hand)
        print(hand)
        
        allCombinations = Algorithm.getAllCombinations(hand)

        allOrganisations = Algorithm.getAllOrganisations(hand, allCombinations)

        allScores = Algorithm.getAllScores(allOrganisations)
        # print(allScores)
        # print(max(allScores))

        bestOrganisation = allOrganisations[allScores.index(max(allScores))]

        temp = []
        for combination in bestOrganisation:
            if combination[1] == 'single':
                temp.append(combination)
        for combination in bestOrganisation:
            if combination[1] != 'single':
                temp.append(combination)
        bestOrganisation = temp
        print(bestOrganisation)

        currentTrick = Algorithm.getCurrentTrickType(state.toBeat)
        
        if currentTrick[0] == 0:
            for combination in bestOrganisation:
                if '3D' in combination[-1]:
                    action = combination[-1]
                    break
            if action == []:
                action = allCombinations[0][-1]

        else:
            for combination in bestOrganisation:
                if combination[0] == currentTrick[0]:
                    if Algorithm.COMBO_ORDER[combination[1]] == Algorithm.COMBO_ORDER[currentTrick[1]]:
                        if Algorithm.RANK_ORDER[combination[2]] > Algorithm.RANK_ORDER[currentTrick[2]]:
                            action = combination[-1]
                            break
                        elif Algorithm.RANK_ORDER[combination[2]] == Algorithm.RANK_ORDER[currentTrick[2]]:
                            if combination[1] == 'flush':
                                result = Algorithm.compareFlushes(combination[-1], Algorithm.sortCards(state.toBeat.cards))
                                if result == 1:
                                    action = combination[-1]
                                    break
                            else:
                                if Algorithm.SUIT_ORDER[combination[3]] > Algorithm.SUIT_ORDER[currentTrick[3]]:
                                    action = combination[-1]
                                    break
                    elif Algorithm.COMBO_ORDER[combination[1]] > Algorithm.COMBO_ORDER[currentTrick[1]]:
                        action = combination[-1]
                        break

        return action, myData