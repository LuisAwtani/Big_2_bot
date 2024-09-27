from classes import *
from collections import defaultdict
from itertools import combinations, product
import math

def print_cards_matrix_debug(CardsInGame):
    # Define rank order for Big 2 (2 at the top down to 3)
    ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
    suits = ['D', 'C', 'H', 'S']  # Diamonds, Clubs, Hearts, Spades
    
    # Create a dictionary to store which cards are still in the game
    cards_left = {rank: {suit: ' ' for suit in suits} for rank in ranks}
    
    # Mark the cards that are still in the game
    for card in CardsInGame:
        rank = card[:-1]  # Get the rank (e.g. "3" from "3H")
        suit = card[-1]   # Get the suit (e.g. "H" from "3H")
        if rank in cards_left and suit in cards_left[rank]:
            # Use 'D', 'C', 'H', 'S' for Diamonds, Clubs, Hearts, Spades
            cards_left[rank][suit] = suit
    
    # Print the matrix header
    print(f"{'Rank':<5} {'Diamonds':<8} {'Clubs':<8} {'Hearts':<8} {'Spades':<8}")
    print('-' * 40)
    
    # Print each row of the matrix (each rank and its available suits)
    for rank in ranks:
        print(f"{rank:<5} {cards_left[rank]['D']:<8} {cards_left[rank]['C']:<8} {cards_left[rank]['H']:<8} {cards_left[rank]['S']:<8}")

class Algorithm:
    COMBO_ORDER = {'straight': 0, 'flush': 1, 'full house': 2, 'four-of-a-kind': 3, 'straight flush': 4}
    RANK_ORDER = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
    SUIT_ORDER = {'?': 0, 'D': 1, 'C': 2, 'H': 3, 'S': 4}
    SCORING = {
        'straight flush': 55,
        'four-of-a-kind': 50,
        'full house': 45,
        'flush': 35,
        'straight': 30,
        'triple': 25,
        'pair': 15,
        'single': 1,
        'bad-single-deduction': 10
    }

    def sortCards(Algorithm, cards): # returns a list of cards sorted by rank and suit
        return sorted(cards, key=lambda card: (Algorithm.RANK_ORDER.get(card[0], 99), Algorithm.SUIT_ORDER.get(card[1], 99)))

    def findPairs(Algorithm, hand):
        pairs = []
        rankDict = defaultdict(list)
        for card in hand:
            rankDict[card[0]].append(card)
        for cards in rankDict.values():
            if len(cards) >= 2:
                for pair in combinations(cards, 2):
                    pairs.append(list(pair))
        return pairs

    def findTriples(Algorithm, hand):
        triples = []
        rankDict = defaultdict(list)
        for card in hand:
            rankDict[card[0]].append(card)
        for cards in rankDict.values():
            if len(cards) >= 3:
                for triple in combinations(cards, 3):
                    triples.append(list(triple))
        return triples
    
    def findStraights(Algorithm, hand):
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
    
    def findFlushes(Algorithm, hand):
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

    def compareFlushes(Algorithm, flush1, flush2):
        flush1 = Algorithm.sortCards(flush1)
        flush2 = Algorithm.sortCards(flush2)
        #print("Comparing flushes...")
        #print("Flush 1: ", flush1)
        #print("Flush 2: ", flush2)
        for i in range(4, -1, -1):
            if Algorithm.RANK_ORDER[flush1[i][0]] > Algorithm.RANK_ORDER[flush2[i][0]]:
                print("Flush 1 wins")
                return True
            elif Algorithm.RANK_ORDER[flush1[i][0]] < Algorithm.RANK_ORDER[flush2[i][0]]:
                print("Flush 2 wins")
                return False
        if Algorithm.SUIT_ORDER[flush1[0][1]] > Algorithm.SUIT_ORDER[flush2[0][1]]:
            print("Flush 1 wins")
            return True
        else:
            print("Flush 2 wins")
            return False

    def findFullHouses(Algorithm, hand):
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

    def findFourOfAKinds(Algorithm, hand):
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

    def findStraightFlushes(Algorithm, hand):
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

    def getAllCombinations(Algorithm, hand): # returns [[type length, type, rank, suit, [cards]]]
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

    def countDeadCards(Algorithm, state: GameHistory):
        thisGame = state.gameHistory
        deadCards = set()
        for listOfTricks in thisGame:
            for trick in listOfTricks:
                for card in trick.cards:
                    deadCards.add(card)
        return deadCards

    def lowestUnanswered(Algorithm, state: MatchState):
        lastTricks = [['2S'], ['2S', '2H'], ['2S', '2H', '2C'], ['2S', 'AS', 'KS', 'QS', 'JS']]
        for round in state.matchHistory[-1].gameHistory:
            # Filter out empty lists (which represent passes)
            nonPassTricks = [trick.cards for trick in round if trick]
            # print("Printing unanswered trick...")
            unansweredTrick = []
            if len(nonPassTricks) >= 3 and not nonPassTricks[-1] and not nonPassTricks[-2] and not nonPassTricks[-3]:
                unansweredTrick = nonPassTricks[-4]
            # print(unansweredTrick)
            # Check if there are any non-pass tricks and get the last one
            if unansweredTrick:
                if len(unansweredTrick) == 1:
                    # print("SINGLE")
                    if Algorithm.S(unansweredTrick[0]) > Algorithm.S(lastTricks[0][0]):
                        lastTricks[0] = unansweredTrick
                elif len(unansweredTrick) == 2:
                    # print("DOUBLE")
                    if Algorithm.isStrongerPair(lastTricks[1], unansweredTrick):
                        lastTricks[1] = unansweredTrick
                elif len(unansweredTrick) == 3:
                    # print("TRIPLE")
                    if Algorithm.isStrongerTriple(lastTricks[2], unansweredTrick):
                        lastTricks[2] = unansweredTrick
                elif len(unansweredTrick) == 5:
                    # print("FIVER")
                    championType, determinant1 = Algorithm.typeOfFiveCardTrick(lastTricks[3])
                    challengerType, determinant2 = Algorithm.typeOfFiveCardTrick(unansweredTrick)
                    if Algorithm.isStrongerTrick(championType, determinant1, challengerType, determinant2, lastTricks[3], unansweredTrick):
                        lastTricks[3] = unansweredTrick
        return lastTricks 

    def S(Algorithm, card: str):
        ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
        suits = ['S', 'H', 'C', 'D']
        rating = ranks.index(card[0]) * 4 + suits.index(card[1])
        return rating
    
    def inverseS(Algorithm, rating: int):
        ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
        suits = ['S', 'H', 'C', 'D']
        index = rating // 4
        suitIndex = rating % 4
        return ranks[index] + suits[suitIndex]

    def Srel(Algorithm, cardinvestigated: str, deadCards: set, copyOfMyHand: list):
        Sval = Algorithm.S(cardinvestigated)
        for deadCard in deadCards:
            if Algorithm.S(deadCard) < Algorithm.S(cardinvestigated):
                Sval -= 1
        hand = sorted(copyOfMyHand, key= lambda x: Algorithm.S(x))
        for carde in hand:
            if Algorithm.S(carde) < Algorithm.S(cardinvestigated):
                Sval -= 1
        return Sval

    def SrelTrick(Algorithm, trick: list, deadCards: set, copyOfMyHand: list):
        if len(trick) == 2:
            cardsInGame = [Algorithm.inverseS(s) for s in range(51) if Algorithm.inverseS(s) not in deadCards and Algorithm.inverseS(s) not in copyOfMyHand]
            strongerPairsInGame = Algorithm.findPairs(cardsInGame)
            quantityOfStrongerPairs = 0
            quantityOfWeakerPairs = 0

            for pairs in strongerPairsInGame:
                if Algorithm.isStrongerPair(pairs, trick):
                    quantityOfStrongerPairs += 1
                else:
                    quantityOfWeakerPairs += 1

            syntheticS = int(math.sqrt(quantityOfStrongerPairs))
            if trick[0][0] == 'A' and syntheticS > 1:
                return 1, quantityOfWeakerPairs // 3
            else:
                return syntheticS, quantityOfWeakerPairs // 3
                # S represents how many stronger pairs are in the game
     
        elif len(trick) == 3:
            cardsInGame = [Algorithm.inverseS(s) for s in range(51) if Algorithm.inverseS(s) not in deadCards and Algorithm.inverseS(s) not in copyOfMyHand]
            inputRankIdx = Algorithm.RANK_ORDER[trick[0][0]]
            rankTriplesCounter = [0 for _ in range(13)]
            belowInputRank = 0
            aboveInputRank = 0
            for card in cardsInGame:
                idx = Algorithm.RANK_ORDER[card[0]]
                rankTriplesCounter[idx] += 1
                if rankTriplesCounter[idx] == 3:
                    if idx < inputRankIdx:
                        belowInputRank += 1
                    else:
                        aboveInputRank += 1
            return aboveInputRank, belowInputRank
        
        elif len(trick) == 5:
 
            trickDetails = Algorithm.typeOfFiveCardTrick(trick)
            if trickDetails[0] == 'straight':
                # If the straight is Jack and lower, it's a codependency
                if Algorithm.S(trickDetails[1]) >= 13:
                    return 4, 0
                else:
                    return 4, 1
            elif trickDetails[0] == 'flush':
                # flushes below jack 
                return 3, 1
            elif trickDetails[0] == 'full house':
                return 1, 1
            # Assume fours and straight flush are unbeatable
            else:
                return 0, 3

    def singleCardPoints(Algorithm, card, deadCards, myHandCopy):
        cardsInGame = 39 - len(deadCards)
        # Assign bonus for strongest card in the game
        if Algorithm.Srel(card, deadCards, myHandCopy) == 0:
            return 30
        elif Algorithm.Srel(card, deadCards, myHandCopy) < 3 and cardsInGame > 12:
            return 20
        elif 3 <= Algorithm.Srel(card, deadCards, myHandCopy) <= 7 and cardsInGame > 18:
            return 8
        elif Algorithm.Srel(card, deadCards, myHandCopy) > 28: # if its one of the worst cards in game
            return -15 - (29 - Algorithm.Srel(card, deadCards, myHandCopy))
        elif Algorithm.Srel(card, deadCards, myHandCopy) > 12:
            return -5
        else:
            # This expression gives favours keeping stronger single cards
            return (1 - (Algorithm.Srel(card, deadCards, myHandCopy) / 39))
 
    def typeOfFiveCardTrick(Algorithm, trick: list):
        Strick = sorted([Algorithm.S(x) for x in trick])
        strongest = Strick[0]
        previous = strongest
        counter = 0

        for i in range(1, 5):
            if Strick[i] == previous + 4:
                previous = Strick[i]
                counter += 1
            else:
                break
        if counter == 4:
            return "straight flush", Algorithm.inverseS(strongest)
        
        cardRanks = [Algorithm.inverseS(x)[0] for x in Strick]
        if len(set(cardRanks)) == 2: # If only 2 ranks exist in the set, Its Fours' of Full House
            if 4 > cardRanks.count(cardRanks[0]) > 1:  # if its a Full House
                if cardRanks[2] != cardRanks[0]:   # Find determining (triplet) rank if its full house
                    return "full house", Algorithm.inverseS(Strick[4])
                else:
                    return "full house", Algorithm.inverseS(strongest)
            else:  # Else we have Four of a kind
                if Algorithm.inverseS(Strick[1])[0] == Algorithm.inverseS(Strick[0])[0]:
                    return "four-of-a-kind", Algorithm.inverseS(Strick[0])
                else:
                    return "four-of-a-kind", Algorithm.inverseS(Strick[1])

        cardSuits = [Algorithm.inverseS(x)[1] for x in Strick]
        if len(set(cardSuits)) == 1:
            return "flush", Algorithm.inverseS(strongest)
        else:
            return "straight", Algorithm.inverseS(strongest)

    def isStrongerTrick(Algorithm, trick1Type, trick1Strongest, trick2Type, trick2Strongest, trick1, trick2):
        # First, compare the trick types
        if Algorithm.COMBO_ORDER[trick1Type] > Algorithm.COMBO_ORDER[trick2Type]:
            return True
        elif Algorithm.COMBO_ORDER[trick1Type] < Algorithm.COMBO_ORDER[trick2Type]:
            return False
        if trick1Type == 'flush':
            return Algorithm.compareFlushes(trick1, trick2)
        # Compare card values first
        if Algorithm.S(trick1Strongest) < Algorithm.S(trick2Strongest):
            return True
        else:
            return False

    def hasOverlap(Algorithm, trick1, trick2):
        """Helper method to check if two tricks overlap (use the same cards)."""
        cards1 = set(trick1[-1])
        cards2 = set(trick2[-1])
        return not cards1.isdisjoint(cards2)

    def findTrickArrangements(Algorithm, allCombinations, hand):
        """Public method that takes tricks as input and finds all valid arrangements."""
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

    def scoreTrick(Algorithm, trick, copyOfMyHand, deadCards, state: MatchState):
        """Score individual tricks based on the rules provided."""
        type_of_trick = trick[1]
        trick_cards = trick[-1]

        score = 0
        if type_of_trick == 'straight flush':
            score += Algorithm.SCORING['straight flush']
        elif type_of_trick == 'four-of-a-kind + single':
            score += Algorithm.SCORING['four-of-a-kind']
        elif type_of_trick == 'full house':
            score += Algorithm.SCORING['full house']
        elif type_of_trick == 'flush':
            score += Algorithm.SCORING['flush']
        elif type_of_trick == 'straight':
            score += Algorithm.SCORING['straight']
        elif type_of_trick == 'triple':
            score += Algorithm.SCORING['triple']
        elif type_of_trick == 'pair':
            score += Algorithm.SCORING['pair']
            # Small amount of bonus points for stronger pair (to avoid strong pair in Full House)
            score += (2 - (2*Algorithm.S(trick[-1][0]) / 51))
            
        elif type_of_trick == 'single':
            # Get the Srel value of the card
            card_value = Algorithm.Srel(trick_cards[0], deadCards, copyOfMyHand)
            score += Algorithm.singleCardPoints(trick_cards[0], deadCards, copyOfMyHand)

        # Apply flexibility bonuses
        if type_of_trick == 'full house':
            score += 5
        elif type_of_trick == 'four-of-a-kind + single':
            score += 3

        return score

    def scoreArrangements(Algorithm, arrangements, copyOfMyHand, deadCards, state: MatchState):
        """Score the entire arrangement and return them sorted by score."""
        scoredArrangements = []
        #print(f"Dead cards being fed into scoreTrick {deadCards}")
        for arrangement in arrangements:
            totalScore = 0
            trickTypes = set()

            # Sum up scores for individual tricks
            for trick in arrangement:
                totalScore += Algorithm.scoreTrick(trick, copyOfMyHand, deadCards, state)
                trickTypes.add(trick[1])

            # Apply diversity bonus for distinct combo types
            totalScore += 2 * len(trickTypes)

            scoredArrangements.append((arrangement, totalScore))

        # Sort by score (descending order)
        scoredArrangements.sort(key=lambda x: x[1], reverse=True)

        return scoredArrangements

    def isStrongerPair(Algorithm, pair1, pair2):
        determinant1 = pair1[0]
        if Algorithm.S(pair1[1]) < Algorithm.S(pair1[0]):
            determinant1 = pair1[1]
        determinant2 = pair2[0]
        if Algorithm.S(pair2[1]) < Algorithm.S(pair2[0]):
            determinant2 = pair2[1]
        if Algorithm.S(determinant1) < Algorithm.S(determinant2):
            return True
        else:
            return False
      
    def isStrongerTriple(Algorithm, triple1, triple2):
        determinant1 = triple1[0]
        determinant2 = triple2[0]
        if Algorithm.S(determinant1) < Algorithm.S(determinant2):
            return True
        else:
            return False

    def countRounds(Algorithm, gameHistory: List[List[Trick]]):
        singleRounds = 0
        pairRounds = 0
        tripleRounds = 0
        fiverRounds = 0
        for round in gameHistory:
            trickSize = len(round[0].cards)
            if trickSize == 1:
                singleRounds += 1
            elif trickSize == 2:
                pairRounds += 1
            elif trickSize == 3:
                tripleRounds += 1
            else:
                fiverRounds += 1
        return singleRounds, pairRounds, tripleRounds, fiverRounds
    
    def playerNumbers(Algorithm, state: MatchState):
        myPlayerNum = state.myPlayerNum  # Player numbers are 0 to 3
        playerAfterMe = (myPlayerNum + 1) % 4
        playerBeforeMe = (myPlayerNum + 3) % 4
        playerOppositeMe = (myPlayerNum + 2) % 4
        playersNotIncludingMe = [playerAfterMe, playerOppositeMe, playerBeforeMe]
        return myPlayerNum, playersNotIncludingMe

    def canBeat(Algorithm, trick: list[str], currentTrick: list[str]):
        # Check if the trick can beat the current trick
        # Return False if the tricks are of different lengths
        # If tricks are of same length, return True if the trick can beat the current trick, and False otherwise
        challengerLen = len(trick)
        championLen = len(currentTrick)
        if challengerLen != championLen:
            return False
        else:
            # If they're both singles, check stronger (lower) S value
            if championLen == 1:
                if Algorithm.S(trick[0]) < Algorithm.S(currentTrick[0]):
                    return True
                else:
                    return False
            #if they're both pairs
            elif championLen == 2:
                if Algorithm.isStrongerPair(trick, currentTrick):
                    return True
                else:
                    return False
            #if they're both triples
            elif championLen == 3:
                if Algorithm.isStrongerTriple(trick, currentTrick):
                    return True
                else:
                    return False
            elif championLen == 5:
                # Determinant refers to the strongest (determining) card in that trick
                challengerTrickType, challengerDeterminant = Algorithm.typeOfFiveCardTrick(trick)
                championTrickType, championDeterminant = Algorithm.typeOfFiveCardTrick(currentTrick)
                if Algorithm.isStrongerTrick(challengerTrickType, challengerDeterminant, championTrickType, championDeterminant, trick, currentTrick):
                    return True
            # No else branch, please notify me if we get return NoneType bug
                else:
                    return False

    # First, pass the current trick on the table as a list of cards.
    # Then, pass the list of non-control tricks and control tricks, where each trick is a list of cards of length 1, 2, 3, or 5.
    # The function returns a boolean indicating whether a winning sequence was found, and the winning sequence if it exists.
    def checkForWinningSequence(Algorithm, currentTrick, nonControlTricks: list[list[str]], controlTricks: list[list[str]]):
            # sort control tricks by length
            controlTricks = sorted(controlTricks, key=len)
            # sort control trick singles by S value, lower S value goes last
            controlTrickSingles = [trick[0] for trick in controlTricks if len(trick) == 1]
            controlTrickSingles = Algorithm.sortCards(controlTrickSingles)
            controlTrickSinglesFinal = []
            for controlTrickSingle in controlTrickSingles:
                controlTrickSinglesFinal.append([controlTrickSingle])
            controlTrickNonSingles = [trick for trick in controlTricks if len(trick) != 1]
            controlTricks = controlTrickNonSingles + controlTrickSinglesFinal
            gameStart = False
            for nonControlTrick in nonControlTricks:
                if '3D' in nonControlTrick:
                    gameStart = True
                    break
            for controlTrick in controlTricks:
                if '3D' in controlTrick:
                    gameStart = True
                    break
            if len(controlTricks) >= len(nonControlTricks) - 1:
                # try to match up one control trick with one non control trick of the same trick length
                    matches = []
                    controlTrickUsed = []
                    for nonControlTrick in nonControlTricks:
                        for i in range(len(controlTricks)):
                            if controlTricks[i] not in controlTrickUsed:
                                if len(controlTricks[i]) == len(nonControlTrick):
                                    matches.append([nonControlTrick, controlTricks[i]])
                                    controlTrickUsed.append(controlTricks[i])
                                    break
                    if len(matches) >= len(nonControlTricks) - 1:
                        winningSequence = []
                        found = False
                        if len(nonControlTricks) == len(controlTricks) + 1: # NCNCNCN
                            for i in range(len(matches)):
                                nonControlTrick = matches[i][0]
                                if currentTrick is None or Algorithm.canBeat(nonControlTrick, currentTrick):
                                    if (gameStart and '3D' in nonControlTrick) or not gameStart:
                                        matches[i], matches[0] = matches[0], matches[i]
                                        found = True
                                        break
                            if found:
                                for match in matches:
                                    winningSequence.append(match[0])
                                    winningSequence.append(match[1])
                                for nonControlTrick in nonControlTricks:
                                    if nonControlTrick not in winningSequence:
                                        winningSequence.append(nonControlTrick)
                                return True, winningSequence
                    
                        elif len(nonControlTricks) == len(controlTricks): # NCNCCN or CNCNCN
                            for i in range(len(matches)):
                                controlTrick = matches[i][1]
                                if currentTrick is None or Algorithm.canBeat(controlTrick, currentTrick):
                                    if (gameStart and '3D' in controlTrick) or not gameStart:
                                        matches[i], matches[0] = matches[0], matches[i]
                                        found = True
                                        break
                            if found and len(matches) == len(nonControlTricks):
                                winningSequence.append(matches[0][1])
                                for i in range(1, len(matches)):
                                    winningSequence.append(matches[i][0])
                                    winningSequence.append(matches[i][1])
                                winningSequence.append(matches[0][0])
                                return True, winningSequence
                            found = False
                            for i in range(len(matches)):
                                nonControlTrick = matches[i][0]
                                if currentTrick is None or Algorithm.canBeat(nonControlTrick, currentTrick):
                                    if (gameStart and '3D' in nonControlTrick) or not gameStart:
                                        matches[i], matches[0] = matches[0], matches[i]
                                        found = True
                                        break
                            if found:
                                for match in matches:
                                    winningSequence.append(match[0])
                                    winningSequence.append(match[1])
                                winningSequence[-2], winningSequence[-1] = winningSequence[-1], winningSequence[-2]
                                for controlTrick in controlTricks:
                                    if controlTrick not in controlTrickUsed:
                                        controlTrickUsed.append(controlTrick)
                                        winningSequence.append(controlTrick)
                                for nonControlTrick in nonControlTricks:
                                    if nonControlTrick not in winningSequence:
                                        winningSequence.append(nonControlTrick)
                                return True, winningSequence

                        else: # CCCCNCNC or NCCCCCNC
                            for controlTrick in controlTricks:
                                if controlTrick not in controlTrickUsed:
                                    if currentTrick is None or Algorithm.canBeat(controlTrick, currentTrick):
                                        if (gameStart and '3D' in controlTrick) or not gameStart:
                                            controlTrickUsed.append(controlTrick)
                                            winningSequence.append(controlTrick)
                                            found = True
                                            break
                            if found:
                                for controlTrick in controlTricks:
                                    if controlTrick not in controlTrickUsed:
                                        controlTrickUsed.append(controlTrick)
                                        winningSequence.append(controlTrick)
                                for match in matches:
                                    winningSequence.append(match[0])
                                    winningSequence.append(match[1])
                                for nonControlTrick in nonControlTricks:
                                    if nonControlTrick not in winningSequence:
                                        winningSequence.append(nonControlTrick)
                                return True, winningSequence
                            for i in range(len(matches)):
                                nonControlTrick = matches[i][0]
                                if currentTrick is None or Algorithm.canBeat(nonControlTrick, currentTrick):
                                    if (gameStart and '3D' in nonControlTrick) or not gameStart:
                                        matches[i], matches[0] = matches[0], matches[i]
                                        found = True
                                        break
                            if found:
                                winningSequence.append(matches[0][0])
                                winningSequence.append(matches[0][1])
                                for controlTrick in controlTricks:
                                    if controlTrick not in controlTrickUsed:
                                        controlTrickUsed.append(controlTrick)
                                        winningSequence.append(controlTrick)
                                for i in range(1, len(matches)):
                                    winningSequence.append(matches[i][0])
                                    winningSequence.append(matches[i][1])
                                for nonControlTrick in nonControlTricks:
                                    if nonControlTrick not in winningSequence:
                                        winningSequence.append(nonControlTrick)
                                return True, winningSequence
            return False, []

    def getAction(Algorithm, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration
        print("Mystic Feng Shui MODEL FINAL")
        print("My Data: ", myData)
        myPlayerNum, PlayersNotIncludingMe = Algorithm.playerNumbers(state)
        deadCards = Algorithm.countDeadCards(state.matchHistory[-1])

        if myData != "" and myData is not None:
            print(f"Previous data: {myData}")

            # Step 1: Remove the brackets (the first and last characters)
            myData = myData[1:-1]

            # Step 2: Split the string by ', ' and remove quotes around each element
            sublist_strings = myData.split("], [")

            # Step 3: Clean up each sublist by removing any extra brackets or quotes and splitting elements
            myDataAsList = []
            for sublist_string in sublist_strings:
                # Remove any remaining square brackets or quotes
                sublist_string = sublist_string.replace('[', '').replace(']', '')
                # Split the sublist into individual elements and strip quotes
                sublist = [element.strip("'") for element in sublist_string.split(", ")]
                # Append the cleaned sublist to the final list
                myDataAsList.append(sublist)

            print(f"Unstringified data: {myDataAsList}")

            if state.toBeat is None:
                action = myDataAsList[0]
                if len(myDataAsList) > 1:
                    myData = str(myDataAsList[1:])
                else:
                    myData = ""
                return action, myData
            else:
                currentTrick = state.toBeat.cards
                if Algorithm.canBeat(myDataAsList[0], currentTrick):
                    if len(myDataAsList) > 1:
                        myData = str(myDataAsList[1:])
                    else:
                        myData = ""
                    action = myDataAsList[0]
                    return action, myData
                else:
                    myData = ""
            
        singleRounds, pairRounds, tripleRounds, fiverRounds = Algorithm.countRounds(state.matchHistory[-1].gameHistory)
        endgame = False
        lossAversion = False

        myHand = state.myHand
        myHand = Algorithm.sortCards(myHand)
        copyOfMyHand = myHand.copy()

        allCombinations = Algorithm.getAllCombinations(myHand)
        validArrangements = Algorithm.findTrickArrangements(allCombinations, copyOfMyHand)
        simplifiedValidArrangements = []

        for arrangement in validArrangements:
            simplifiedArrangement = []
            for trick in arrangement:
                simplifiedArrangement.append(trick[-1])
            simplifiedValidArrangements.append(simplifiedArrangement)

        print("My Hand: ", myHand)

        #print(f"DeadCards being fed into scoreArrangements {deadCards}")
        scoredArrangements = Algorithm.scoreArrangements(validArrangements, copyOfMyHand, deadCards, state)
        
        # print("The top 3 arrangements: ")
        # print(" \n ")
        # print(scoredArrangements[0])
        # if len(scoredArrangements) > 3:
        #    print(" \n ")
        #    print(scoredArrangements[1])
        #    print(" \n ")
        #    print(scoredArrangements[2])

        singles = [trick[4] for trick in scoredArrangements[0][0] if trick[1] == 'single']
        pairs = [trick[4] for trick in scoredArrangements[0][0] if trick[1] == 'pair']
        triples = [trick[4] for trick in scoredArrangements[0][0] if trick[1] == 'triple']
        fives = [trick[4] for trick in scoredArrangements[0][0] if trick[1] != 'triple' and trick[1] != 'pair' and trick[1] != 'single']
       
        strategy = singles + pairs + triples + fives    
                        


        lowestUnansweredTricks = Algorithm.lowestUnanswered(state)
        print(f"strategy : {strategy}")
        mustBeForced = []
        potentialControlCards = []
        controlCards = []
        if len(singles) > 0:
            for i in range(len(singles)):
                Sval = Algorithm.Srel(singles[i][0], deadCards, copyOfMyHand)
                if Sval <= 0:
                    controlCards.append(singles[i])
                elif Sval < 4 and (51 - len(deadCards) - len(copyOfMyHand)):
                    potentialControlCards.append(singles[i])
                elif Sval >= (39 - len(deadCards) - 5):
                    mustBeForced.append(singles[i])

        if len(pairs) > 0:
            for i in range(len(pairs)):
                strongerWeaker = Algorithm.SrelTrick(pairs[i], deadCards, copyOfMyHand)
                if strongerWeaker[0] <= 1:
                    controlCards.append(pairs[i])
                elif strongerWeaker[0] <= 3:
                    potentialControlCards.append(pairs[i])
                if strongerWeaker[1] < 4:
                    mustBeForced.append(pairs[i])
                
                if Algorithm.isStrongerPair(pairs[i], lowestUnansweredTricks[1]):
                    if pairs[i] not in controlCards and pairs[i] not in potentialControlCards:
                        potentialControlCards.append(pairs[i])

        if len(triples) > 0:
            #print(f"My first triple has S value of [stronger, weaker] {Algorithm.SrelTrick(triples[0], deadCards, copyOfMyHand)}")
            for i in range(len(triples)):
                strongerWeakerThrees = Algorithm.SrelTrick(triples[i], deadCards, copyOfMyHand)
                if strongerWeakerThrees[0] <= 2:
                    controlCards.append(triples[i])
                elif strongerWeakerThrees[1] <= 3:
                    mustBeForced.append(triples[i])
                if strongerWeakerThrees[0] <= 5:
                    potentialControlCards.append(triples[i])
                
                if Algorithm.isStrongerTriple(triples[i], lowestUnansweredTricks[2]):
                    if triples[i] not in controlCards:
                        controlCards.append(triples[i])
                        if triples[i] in potentialControlCards:
                            potentialControlCards.remove(triples[i])

        if len(fives) > 0:
            for i in range(len(fives)):
                strongerWeakerFives = Algorithm.SrelTrick(fives[i], deadCards, copyOfMyHand)
                if strongerWeakerFives[0] == 0:
                    controlCards.append(fives[i])
                elif strongerWeakerFives[0] == 1:
                    potentialControlCards.append(fives[i])
                elif strongerWeakerFives[1] == 0:
                    mustBeForced.append(fives[i])

                trick1Type, trick1Determinant = Algorithm.typeOfFiveCardTrick(fives[i])
                trick2Type, trick2Determinant = Algorithm.typeOfFiveCardTrick(lowestUnansweredTricks[3])

                # If a previosu weaker 5 card went unbeaten, this becomes a control card trick
                if Algorithm.isStrongerTrick(trick1Type, trick1Determinant, trick2Type, trick2Determinant, fives[i], lowestUnansweredTricks[3]):
                    if fives[i] not in controlCards:
                        controlCards.append(fives[i])

                counter = 0
                for playerNum in PlayersNotIncludingMe:
                    if state.players[playerNum].handSize <= 5:
                        counter += 1
                if counter >= 2:
                    if fives[i] not in controlCards:
                        controlCards.append(fives[i])
                    if fives[i] not in mustBeForced:
                        mustBeForced.append(fives[i])
            # All fives must be forced if we missed a 5 card trick round
            if fiverRounds > 0 and state.toBeat is not None:
                if len(state.toBeat.cards) != 5:
                    for trick in fives:
                        if trick not in mustBeForced:
                            mustBeForced.append(trick)
 
        print(f"These tricks are so weak they must be forced: {mustBeForced}")
        print(f"These tricks might be control cards {potentialControlCards}")
        print(f"These tricks are definitely control cards: {controlCards}")
        #print(f"\nThese were the lowest unanswered tricks played: {Algorithm.lowestUnanswered(state)}")

        if len(controlCards) >= (len(strategy) / 2):
            #print(f"{len(strategy)} plays left, {len(controlCards)} are controlCards, {len(potentialControlCards)} are potential controlCards")
            non_control_tricks = [trick for trick in strategy if trick not in controlCards and trick not in potentialControlCards]
            if state.toBeat is not None:
                currentTrick = state.toBeat.cards
            else:
                currentTrick = None
            print("Checking for deterministic winning combo")
            winningSequence = Algorithm.checkForWinningSequence(currentTrick, non_control_tricks, controlCards + potentialControlCards)
            if winningSequence[0] is True:
                print("Winning sequence found")
                print("Non-control tricks considered: ", non_control_tricks)
                print("Control tricks considered: ", controlCards)
                print("Potential control tricks considered: ", potentialControlCards)
                print("Winning sequence: ", winningSequence)
            endgame = True

        elif len(potentialControlCards) + len(controlCards) >= ((len(strategy)) / 2):

            #print(f"{len(strategy)} plays left, {len(controlCards)} are controlCards, {len(potentialControlCards)} are potential controlCards")
            non_control_tricks = [trick for trick in strategy if trick not in controlCards and trick not in potentialControlCards]
            if state.toBeat is not None:
                currentTrick = state.toBeat.cards
            else:
                currentTrick = None
            print("Checking for probabilistic winning combo")
            winningSequence = Algorithm.checkForWinningSequence(currentTrick, non_control_tricks, controlCards + potentialControlCards)
            if winningSequence[0] is True:
                print("Winning sequence found")
                print("Non-control tricks considered: ", non_control_tricks)
                print("Control tricks considered: ", controlCards)
                print("Potential control tricks considered: ", potentialControlCards)
                print("Winning sequence: ", winningSequence)
            endgame = True

        tally = 0
        for playerNum in PlayersNotIncludingMe:
            if state.players[playerNum].handSize < 3:
                lossAversion = True
                print(f"ENTERING Loss aversion mode, player {playerNum} has {state.players[playerNum].handSize} cards left")
                if state.players[playerNum].handSize <=3:
                    tally += 1
        if tally >= 2 and lossAversion is False:
            lossAversion = True
            print(" ENTERING LOSS AVERSION TWO PLAYERS WITH 3 OR LESS CARDS")

        if '3D' in myHand:
            for trick in strategy:
                if '3D' in trick:
                    action = trick
        
        elif state.toBeat is None:
            # Play weakest high order trick
            # if we have a high order control trick, play that
            if len(mustBeForced) > 0:
                maxLen = 0
                # PLay the weakest must force of the largest trick type
                for i in range(len(mustBeForced)):
                    if len(mustBeForced[i]) > maxLen:
                        action = mustBeForced[i]
                        maxLen = len(mustBeForced[i])
                        

                if lossAversion is True: # Check that we aren't playing a very weak single
                    if len(action) == 1:
                        print(f"Attepting to prevent foolish loss aversion with {action[0]}")
                        if action[0] in mustBeForced:
                            print("PREVENTING PLAYING VERY WEAK SINGLE")
                            action = strategy[-1]
                    elif len(action) == 2:
                        if action in controlCards:
                            print("Edge Case loss Aversion pair")
                            controlPairs = [t for t in controlCards if len(t) == 2]
                            action = controlPairs[-1]
                    
                # If we have a high order potential control card (with no low order) play that instead
                if len(action) == 0:
                    if len(potentialControlCards + controlCards) > 0:
                        minlen = 6
                        for tricke in potentialControlCards + controlCards:
                            if len(tricke) < minlen:
                                minlen = len(tricke)
                        if minlen > 1:
                            for tricke in potentialControlCards + controlCards:
                                if len(tricke) == minlen:
                                    action = tricke

            else:
                for trick in strategy:
                    if len(fives) > 0:
                        action = strategy[-len(fives)]
                    elif len(triples) > 0:
                        action = strategy[-len(triples)]
                    elif len(pairs) > 0:
                        action = strategy[-len(pairs)]
                    else:
                        if lossAversion is True:
                            action = strategy[-1]
                        else:
                            action = strategy[0]
        
        elif len(state.toBeat.cards) == 1:
            StoBeat = Algorithm.S(state.toBeat.cards[0])
            if lossAversion is False:
                for i in range(len(singles)):
                    if Algorithm.S(strategy[i][0]) < StoBeat:
                        action = strategy[i]
                        break
                if len(action) > 0:
                    if action in potentialControlCards and controlCards:
                        if len(controlCards[0]) == 1:
                            print(f"Sparing potential control card {action} for control card {controlCards}")
                            action = controlCards[0]
            else:
                if Algorithm.S(copyOfMyHand[-1]) < StoBeat: # PLay strongest card if I can
                    action.append(copyOfMyHand[-1])

            # If i'm about to play a potential control card, play the control card instead
            # if action:
                #if action[0] in potentialControlCards and controlCards:
                    
        elif len(state.toBeat.cards) == 2:
            for i in range(len(singles),len(singles) + len(pairs)):
                if Algorithm.isStrongerPair(strategy[i], state.toBeat.cards):
                    action = strategy[i]
                    break
            # consider breaking up full house in case of loss aversion    
            if lossAversion is True:
                print("Pair loss aversion")
                if len(action) == 0:
                    toUse = singles + triples
                    for fiveCardTrick in fives:
                        type, deter = Algorithm.typeOfFiveCardTrick(fiveCardTrick)
                        if type == 'full house':
                            toUse.extend(fiveCardTrick)

                    toUse = singles + triples
                    print(f"Cards to use {toUse}")
                    extraPairs = Algorithm.findPairs(toUse)
                    print(f"Extra pairs found: {extraPairs}")
                    if len(extraPairs) == 0:
                        toUse = singles + triples + fives
                        extraPairs = Algorithm.findPairs(toUse)
                    for extraPair in extraPairs:
                        if Algorithm.isStrongerPair(extraPair, state.toBeat.cards):
                            action = extraPair

        elif len(state.toBeat.cards) == 3:
            for i in range(len(singles) + len(pairs), len(singles) + len(pairs) + len(triples)):
                if Algorithm.isStrongerTriple(strategy[i], state.toBeat.cards):
                    action = strategy[i]
                    break   
                if lossAversion is True:
                    if len(action) == 0:
                        extraTriples = Algorithm.findTriples(fives)
                        for triple in extraTriples:
                            if Algorithm.isStrongerTriple(triple, state.toBeat.cards):
                                action = triple             

        elif len(state.toBeat.cards) == 5:
            print(f"This is the {fiverRounds} fives round")
            if len(fives) > 0:
                trickType, determinant = Algorithm.typeOfFiveCardTrick(state.toBeat.cards)
                for i in range(len(fives)):
                    challengerTrickType, challengerDeterminant = Algorithm.typeOfFiveCardTrick(strategy[-1-i])
                    #print("DEBUG IF I AM ABOUT TO PLAY A FIVE COMPARE TO toBeat")
                    if Algorithm.isStrongerTrick(challengerTrickType, challengerDeterminant, trickType, determinant, strategy[-1-i], state.toBeat.cards):
                        action = strategy[-i-1]
                        break
            if len(action) == 0:
                if len(singles) >= 5:
                    singleCards = [single[0] for single in singles]
                    print(f"Inputting singles: {singleCards}")
                    extraStraights = Algorithm.findStraights(singleCards)
                    if len(extraStraights) > 0:
                        trickType, determinant = Algorithm.typeOfFiveCardTrick(state.toBeat.cards)
                        xTraType, xTraDeterminant = Algorithm.typeOfFiveCardTrick(extraStraights[0])
                        if Algorithm.isStrongerTrick(xTraType, xTraDeterminant, trickType, determinant, extraStraights[0], state.toBeat.cards):
                            action = extraStraights[0]
                            print("Found extra straight")
            
        if endgame is True:
            if winningSequence[0] is True:
                print(f"Committing to winning sequence: {winningSequence}")
                action = winningSequence[1][0]
                # put the winning sequence in myData except the first element, stringified
                if len(winningSequence[1]) > 1:
                    myData = str(winningSequence[1][1:])
                else:
                    myData = ""
        return action, myData