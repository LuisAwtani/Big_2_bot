from classes import *
from collections import Counter, defaultdict
from itertools import combinations, product

class Algorithm:
    COMBO_ORDER = {'single': 0, 'pair': 1, 'triple': 2, 'straight': 3, 'flush': 4, 'full house': 5, 'four-of-a-kind': 6, 'straight flush': 7}
    RANK_ORDER = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
    SUIT_ORDER = {'?': 0, 'D': 1, 'C': 2, 'H': 3, 'S': 4}
    SCORING = {
        'single': 5,
        'single_two': 7,
        'pair': 12,
        'triple': 18,
        'straight': 28,
        'flush': 30,
        'full house': 35,
        'four-of-a-kind': 40,
        'straight flush': 45,
        'control_use_penalty': 10  # Penalty for using control cards above their control level
    }

    @staticmethod
    def sortCards(cards):  # Returns a list of cards sorted by rank and suit
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
    def isTooFarBehind(players, myPlayerNum):
        myHandSize = players[myPlayerNum].handSize
        otherHandSizes = []
        for i in range(0, 4):
            if i != myPlayerNum:
                otherHandSizes.append(players[i].handSize)
        averageOtherHandSize = sum(otherHandSizes) / len(otherHandSizes)
        threshold = 3  # Adjust this threshold as needed

        if myHandSize - averageOtherHandSize >= threshold:
            return True
        return False


    @staticmethod
    def isOpponentAboutToWin(players, myPlayerNum):
        for i in range(0, 4):
            print(players[i].handSize)
            if players[i].handSize <= 2 and i != myPlayerNum:
                return True
        return False


    @staticmethod
    def canPlay(organisation, currentTrick):
        if currentTrick[0] == 0:
            return True
        else:
            for combination in organisation:
                if combination[0] == currentTrick[0]:
                    if Algorithm.COMBO_ORDER[combination[1]] == Algorithm.COMBO_ORDER[currentTrick[1]]:
                        if Algorithm.RANK_ORDER[combination[2]] > Algorithm.RANK_ORDER[currentTrick[2]]:
                            return True
                        elif Algorithm.RANK_ORDER[combination[2]] == Algorithm.RANK_ORDER[currentTrick[2]]:
                            if Algorithm.SUIT_ORDER[combination[3]] > Algorithm.SUIT_ORDER[currentTrick[3]]:
                                return True
                    elif Algorithm.COMBO_ORDER[combination[1]] > Algorithm.COMBO_ORDER[currentTrick[1]]:
                        return True


    @staticmethod
    def getRemainingCards(fullDeck, playerHand, gameHistory):
        # Remove player's hand and played cards from the full deck
        playedCards = set()
        for round in gameHistory.gameHistory:
            for trick in round:
                playedCards.update(trick.cards)
        remainingCards = set(fullDeck) - set(playerHand) - playedCards
        return list(remainingCards)


    @staticmethod
    def isControlSingle(card, remainingCards):
        cardRank = Algorithm.RANK_ORDER[card[0]]
        cardSuit = Algorithm.SUIT_ORDER[card[1]]
        for oppCard in remainingCards:
            oppRank = Algorithm.RANK_ORDER[oppCard[0]]
            oppSuit = Algorithm.SUIT_ORDER[oppCard[1]]
            if oppRank > cardRank:
                return False
            elif oppRank == cardRank and oppSuit > cardSuit:
                return False
        return True


    @staticmethod
    def isControlPair(pairCards, remainingCards):
        cardRank = pairCards[0][0]
        cardRankValue = Algorithm.RANK_ORDER[cardRank]
        remainingRanks = [card[0] for card in remainingCards]
        remainingRankCounts = Counter(remainingRanks)
        for oppRank, count in remainingRankCounts.items():
            oppRankValue = Algorithm.RANK_ORDER[oppRank]
            if count >= 2:
                if oppRankValue > cardRankValue:
                    return False
                elif oppRankValue == cardRankValue:
                    oppSuits = [card[1] for card in remainingCards if card[0] == oppRank]
                    maxOppSuit = max(Algorithm.SUIT_ORDER[suit] for suit in oppSuits)
                    maxCardSuit = max(Algorithm.SUIT_ORDER[card[1]] for card in pairCards)
                    if maxOppSuit > maxCardSuit:
                        return False
        return True


    @staticmethod
    def isControlTriple(tripleCards, remainingCards):
        cardRank = tripleCards[0][0]
        cardRankValue = Algorithm.RANK_ORDER[cardRank]
        remainingRanks = [card[0] for card in remainingCards]
        remainingRankCounts = Counter(remainingRanks)
        for oppRank, count in remainingRankCounts.items():
            oppRankValue = Algorithm.RANK_ORDER[oppRank]
            if count >= 3:
                if oppRankValue > cardRankValue:
                    return False
        return True


    @staticmethod
    def getControlLevels(playerHand, remainingCards):
        controlLevels = {}
        for card in playerHand:
            # Initially, assume the card is not a control
            controlLevels[card] = None
            # Check if the card is a control single
            if Algorithm.isControlSingle(card, remainingCards):
                controlLevels[card] = 'single'

        # Check for control pairs
        rankDict = defaultdict(list)
        for card in playerHand:
            rankDict[card[0]].append(card)
        for rank, cards in rankDict.items():
            if len(cards) >= 2:
                pairCards = cards[:2]
                if Algorithm.isControlPair(pairCards, remainingCards):
                    for card in pairCards:
                        # Update control level to 'pair' if higher than current
                        if controlLevels[card] != 'single':
                            controlLevels[card] = 'pair'

        # Check for control triples
        for rank, cards in rankDict.items():
            if len(cards) >= 3:
                tripleCards = cards[:3]
                if Algorithm.isControlTriple(tripleCards, remainingCards):
                    for card in tripleCards:
                        # Update control level to 'triple' if higher than current
                        if controlLevels[card] not in ['single', 'pair']:
                            controlLevels[card] = 'triple'

        return controlLevels


    @staticmethod
    def getAllScores(allOrganisations, currentTrick, gameHistory, playerHand, ignoreControlPenalties=False, mustPlay=False):
        scores = []
        # Build the full deck
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        fullDeck = [rank + suit for rank in ranks for suit in suits]

        # Get remaining cards
        remainingCards = Algorithm.getRemainingCards(fullDeck, playerHand, gameHistory)

        # Get control levels for each card in the player's hand
        controlLevels = Algorithm.getControlLevels(playerHand, remainingCards)

        playabilityBonus = 50 if mustPlay else 0

        for organisation in allOrganisations:
            score = 0
            for combination in organisation:
                comboType = combination[1]
                comboLevel = comboType  # The level at which the combination is played
                cards = combination[-1]  # List of cards in the combination

                # Base score for the combination
                if comboType == 'single' and cards[0][0] == '2':
                    baseScore = Algorithm.SCORING['single_two']
                else:
                    baseScore = Algorithm.SCORING[comboType]

                # Initialize penalty
                totalPenalty = 0

                if not ignoreControlPenalties:
                    # Check if any control cards are used above their control level
                    for card in cards:
                        controlLevel = controlLevels.get(card)
                        if controlLevel:
                            controlLevelValue = Algorithm.COMBO_ORDER[controlLevel]
                            comboLevelValue = Algorithm.COMBO_ORDER[comboLevel]
                            if comboLevelValue > controlLevelValue:
                                # Apply penalty for using control card above its control level
                                totalPenalty += Algorithm.SCORING['control_use_penalty']

                # Additional penalties for full houses and four-of-a-kind
                if comboType == 'full house':
                    # Extract the pair rank
                    cardRanks = [card[0] for card in cards]
                    rankCounts = Counter(cardRanks)
                    pairRank = [rank for rank, count in rankCounts.items() if count == 2][0]
                    pairRankValue = Algorithm.RANK_ORDER[pairRank]
                    # Apply penalty based on pair rank
                    totalPenalty += pairRankValue * 0.5
                elif comboType == 'four-of-a-kind':
                    # Extract the kicker rank
                    cardRanks = [card[0] for card in cards]
                    rankCounts = Counter(cardRanks)
                    kickerRank = [rank for rank, count in rankCounts.items() if count == 1][0]
                    kickerRankValue = Algorithm.RANK_ORDER[kickerRank]
                    # Apply penalty based on kicker rank
                    totalPenalty += kickerRankValue * 0.5

                totalComboScore = baseScore - totalPenalty
                score += totalComboScore

            if mustPlay and Algorithm.canPlay(organisation, currentTrick):
                score += playabilityBonus

            scores.append(score)
        return scores


    @staticmethod
    def getPossibleOpponentPairs(remainingCards):
        rankCounts = Counter(card[0] for card in remainingCards)
        opponentPairs = []
        for rank, count in rankCounts.items():
            if count >= 2:
                suits = [card[1] for card in remainingCards if card[0] == rank]
                for suitPair in combinations(suits, 2):
                    opponentPairs.append((rank, suitPair))
        return opponentPairs


    @staticmethod
    def getPossibleOpponentTriples(remainingCards):
        rankCounts = Counter(card[0] for card in remainingCards)
        opponentTriples = []
        for rank, count in rankCounts.items():
            if count >= 3:
                suits = [card[1] for card in remainingCards if card[0] == rank]
                for suitTriple in combinations(suits, 3):
                    opponentTriples.append((rank, suitTriple))
        return opponentTriples


    @staticmethod
    def containsControlCards(combination, playerHand, gameHistory):
        # Build the full deck
        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        fullDeck = [rank + suit for rank in ranks for suit in suits]

        # Get remaining cards
        remainingCards = Algorithm.getRemainingCards(fullDeck, playerHand, gameHistory)

        # Get control levels for each card in the player's hand
        controlLevels = Algorithm.getControlLevels(playerHand, remainingCards)

        # Check if any card in the combination is a control card
        for card in combination[-1]:
            if card in controlLevels and controlLevels[card] is not None:
                return True
        return False


    @staticmethod
    def getStartOnlyCombinations(bestOrganisation, remainingCards):
        startOnlyCombinations = []

        # Generate possible opponent combinations
        opponentSingles = remainingCards
        opponentPairs = Algorithm.getPossibleOpponentPairs(remainingCards)
        opponentTriples = Algorithm.getPossibleOpponentTriples(remainingCards)
        # For five-card combinations, we can generate possible opponent combinations if necessary

        for combination in bestOrganisation:
            comboType = combination[1]
            comboRank = combination[2]
            comboSuit = combination[3]
            cards = combination[-1]

            canBeatOpponent = False

            if comboType == 'single':
                for oppCard in opponentSingles:
                    if Algorithm.RANK_ORDER[comboRank] > Algorithm.RANK_ORDER[oppCard[0]]:
                        canBeatOpponent = True
                        break
                    elif Algorithm.RANK_ORDER[comboRank] == Algorithm.RANK_ORDER[oppCard[0]]:
                        if Algorithm.SUIT_ORDER[comboSuit] > Algorithm.SUIT_ORDER[oppCard[1]]:
                            canBeatOpponent = True
                            break

            elif comboType == 'pair':
                for oppPair in opponentPairs:
                    oppRank = oppPair[0]
                    oppSuits = oppPair[1]
                    if Algorithm.RANK_ORDER[comboRank] > Algorithm.RANK_ORDER[oppRank]:
                        canBeatOpponent = True
                        break
                    elif Algorithm.RANK_ORDER[comboRank] == Algorithm.RANK_ORDER[oppRank]:
                        maxComboSuit = max(Algorithm.SUIT_ORDER[card[1]] for card in cards)
                        maxOppSuit = max(Algorithm.SUIT_ORDER[suit] for suit in oppSuits)
                        if maxComboSuit > maxOppSuit:
                            canBeatOpponent = True
                            break

            elif comboType == 'triple':
                for oppTriple in Algorithm.getPossibleOpponentTriples(remainingCards):
                    oppRank = oppTriple[0]
                    if Algorithm.RANK_ORDER[comboRank] > Algorithm.RANK_ORDER[oppRank]:
                        canBeatOpponent = True
                        break

            # For simplicity, we'll consider five-card combinations as always potentially playable
            else:
                canBeatOpponent = True

            if not canBeatOpponent:
                startOnlyCombinations.append(combination)

        return startOnlyCombinations


    def getAction(Algorithm, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration

        # TODO Write your algorithm logic here

        print("LEXICON FINAL MODEL")

        hand = state.myHand
        hand = Algorithm.sortCards(hand)
        print(hand)
        
        allCombinations = Algorithm.getAllCombinations(hand)

        allOrganisations = Algorithm.getAllOrganisations(hand, allCombinations)

        currentTrick = Algorithm.getCurrentTrickType(state.toBeat)

        tooFarBehind = Algorithm.isTooFarBehind(state.players, state.myPlayerNum)
        opponentAboutToWin = Algorithm.isOpponentAboutToWin(state.players, state.myPlayerNum)
        print("TooFarBehind: ", tooFarBehind) 
        print("OpponentAboutToWin: ", opponentAboutToWin)
        print("PlayerNum: ", state.myPlayerNum)

        allScores = Algorithm.getAllScores(allOrganisations, currentTrick, state.matchHistory[-1], hand, ignoreControlPenalties=opponentAboutToWin, mustPlay=tooFarBehind)
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

        ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
        suits = ['D', 'C', 'H', 'S']
        fullDeck = [rank + suit for rank in ranks for suit in suits]
        remainingCards = Algorithm.getRemainingCards(fullDeck, hand, state.matchHistory[-1])

        # Get combinations that can only be played when starting
        startOnlyCombinations = Algorithm.getStartOnlyCombinations(bestOrganisation, remainingCards)
        
        resistPlayingControl = False
        if not startOnlyCombinations:
            resistPlayingControl = True

        if not opponentAboutToWin:
            if currentTrick[0] == 0:
                for combination in bestOrganisation:
                    if '3D' in combination[-1]:
                        action = combination[-1]
                        break
                if action == []:
                    if startOnlyCombinations != []:
                        action = startOnlyCombinations[0][-1]
                        print("Start Only Combination")
                if action == []:
                    for combination in bestOrganisation:
                        if combination[0] == 5:
                            action = combination[-1]
                            break
                if action == []:
                    for combination in bestOrganisation:
                        if combination[0] == 3:
                            action = combination[-1]
                            break
                if action == []:
                    for combination in bestOrganisation:
                        if combination[0] == 2:
                            action = combination[-1]
                            break
                if action == []:
                    for combination in bestOrganisation:
                        if combination[0] == 1:
                            action = combination[-1]
                            break
            else:
                for combination in bestOrganisation:
                    if resistPlayingControl and Algorithm.containsControlCards(combination, hand, state.matchHistory[-1]):
                        continue
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
        else:
            if currentTrick[0] == 0:
                action = bestOrganisation[-1][-1]
            else:
                for combination in bestOrganisation:
                    if combination[0] == currentTrick[0]:
                        if Algorithm.COMBO_ORDER[combination[1]] == Algorithm.COMBO_ORDER[currentTrick[1]]:
                            if Algorithm.RANK_ORDER[combination[2]] > Algorithm.RANK_ORDER[currentTrick[2]]:
                                action = combination[-1]
                            elif Algorithm.RANK_ORDER[combination[2]] == Algorithm.RANK_ORDER[currentTrick[2]]:
                                if combination[1] == 'flush':
                                    result = Algorithm.compareFlushes(combination[-1], Algorithm.sortCards(state.toBeat.cards))
                                    if result == 1:
                                        action = combination[-1]
                                else:
                                    if Algorithm.SUIT_ORDER[combination[3]] > Algorithm.SUIT_ORDER[currentTrick[3]]:
                                        action = combination[-1]
                        elif Algorithm.COMBO_ORDER[combination[1]] > Algorithm.COMBO_ORDER[currentTrick[1]]:
                            action = combination[-1]

        return action, myData