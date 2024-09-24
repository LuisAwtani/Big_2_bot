from classes import *
from collections import defaultdict
from itertools import combinations, product
import random
import math

SCORING = {
    'straight flush': 55,
    'four-of-a-kind': 50,
    'full house': 45,
    'flush': 35,
    'straight': 30,
    'triple': 20,
    'pair': 15,
    'single': 1,
    'bad-single-deduction': 10
}

rank_order = {
    '3': 0, '4': 1, '5': 2, '6': 3, '7': 4,
    '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9,
    'K': 10, 'A': 11, '2': 12  # '2' is the highest rank in Big 2
}

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
    combinationOrder = {'single': 0, 'pair': 1, 'triple': 2, 'straight': 3, 'flush': 4, 'full house': 5, 'four-of-a-kind': 6, 'straight flush': 7}
    rankOrder = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
    suitOrder = {'?': 0, 'D': 1, 'C': 2, 'H': 3, 'S': 4}


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
    def compareFlushes(flush1, flush2):
        for i in range(4, -1, -1):
            if Algorithm.rankOrder[flush1[i][0]] > Algorithm.rankOrder[flush2[i][0]]:
                return 1
            elif Algorithm.rankOrder[flush1[i][0]] < Algorithm.rankOrder[flush2[i][0]]:
                return 0
        if Algorithm.suitOrder[flush1[0][1]] > Algorithm.suitOrder[flush2[0][1]]:
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
    def getCurrentTrickType(trick: Trick): # returns [type length, type, rank to beat, suit to beat]
        if trick is None:
            return [0, 'start']
        else:
            trick = Algorithm.sortCards(trick.cards)
            if len(trick) == 5:
                if trick[0][1] == trick[1][1] == trick[2][1] == trick[3][1] == trick[4][1]:
                    if Algorithm.rankOrder[trick[0][0]] == Algorithm.rankOrder[trick[1][0]] - 1 == Algorithm.rankOrder[trick[2][0]] - 2 == Algorithm.rankOrder[trick[3][0]] - 3 == Algorithm.rankOrder[trick[4][0]] - 4:
                        return [5, 'straight flush', trick[4][0], trick[4][1]]
                    else:
                        return [5, 'flush', trick[4][0], trick[4][1]]
                elif Algorithm.rankOrder[trick[0][0]] == Algorithm.rankOrder[trick[1][0]] - 1 == Algorithm.rankOrder[trick[2][0]] - 2 == Algorithm.rankOrder[trick[3][0]] - 3 == Algorithm.rankOrder[trick[4][0]] - 4:
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


    def countDeadCards(Algorithm, state: GameHistory):
        ThisGame = state.gameHistory
        deadCards = set()
        for x in ThisGame:
            for y in x:
                for card in y.cards:
                    deadCards.add(card)
        return deadCards


    def S(Algorithm, Card: str):
        ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
        suits = ['S', 'H', 'C', 'D']
        rating = ranks.index(Card[0]) * 4 + suits.index(Card[1])
        return rating
    
    def inverseS(self, rating: int):
        ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
        suits = ['S', 'H', 'C', 'D']
        index = rating // 4
        suitIndex = rating % 4
        return ranks[index] + suits[suitIndex]

    def Srel(Algorithm, Card: str, deadCards: set, copyofMyHand: list):
        Sval = Algorithm.S(Card)
        for deadCard in deadCards:
            if Algorithm.S(deadCard) < Sval:
                Sval -= 1

        Hand = sorted(copyofMyHand, reverse=True)
        Hand.remove(Card)

        for x in Hand:
            if Algorithm.S(x) < Algorithm.S(Card):
                Sval -= 1
        return Sval
    
    def SrelTrick(Algorithm, trick: list, deadCards: set, copyofMyHand: list):
        if len(trick) == 2:
            cardsInGame = [Algorithm.inverseS(s) for s in range(51) if Algorithm.inverseS(s) not in deadCards and Algorithm.inverseS(s) not in copyofMyHand]
            strongerPairsInGame = Algorithm.findPairs(cardsInGame)
            quantityofStrongerPairs = 0
            quantityofWeakerPairs = 0

            for pairs in strongerPairsInGame:
                if Algorithm.is_stronger_pair(pairs, trick):
                    quantityofStrongerPairs += 1
                else:
                    quantityofWeakerPairs += 1

            syntheticS = int(math.sqrt(quantityofStrongerPairs))
            if trick[0][0] == 'A' and syntheticS > 1:
                return 1, quantityofWeakerPairs // 3
            else:
                if syntheticS > 3:
                    return syntheticS, quantityofWeakerPairs // 3
                else:
                    return syntheticS, quantityofWeakerPairs // 3
                # S represents how many stronger pairs are in the game
     
        elif len(trick) == 3:
            cardsInGame = [Algorithm.inverseS(s) for s in range(51) if Algorithm.inverseS(s) not in deadCards and Algorithm.inverseS(s) not in copyofMyHand]
            inputRankIdx = rank_order[trick[0][0]]
            rankTriplesCounter = [0 for _ in range(13)]
            belowInputRank = 0
            aboveInputRank = 0
            for card in cardsInGame:
                idx = rank_order[card[0]]
                rankTriplesCounter[idx] += 1
                if rankTriplesCounter[idx] == 3:
                    if idx < inputRankIdx:
                        belowInputRank += 1
                    else:
                        aboveInputRank += 1
            return aboveInputRank, belowInputRank
        
        elif len(trick) == 5:
            return 1, 1
    
    def get_rank(Algorithm, card):
        rank = card[:-1]  # Remove the suit (last character)
        return rank_order[rank]


    def single_card_points(Algorithm, card, deadCards, myHandCopy):
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

    def check_stronger_flush(flush1, flush2):
        # Sort both flushes by rank in descending order
        flush1_sorted = sorted(flush1, key=lambda card: Algorithm.get_rank(card), reverse=True)
        flush2_sorted = sorted(flush2, key=lambda card: Algorithm.get_rank(card), reverse=True)

        # Compare each card rank in order from highest to lowest
        for card1, card2 in zip(flush1_sorted, flush2_sorted):
            if Algorithm.get_rank(card1) > Algorithm.get_rank(card2):
                return True
            elif Algorithm.get_rank(card1) < Algorithm.get_rank(card2):
                return False

        # If all cards are the same in terms of rank, return False (the flushes are equal in strength)
        print("Fluhes are equal in strength")
        return True

    
    def TypeOfFiveCardTrick(Algorithm, trick: list):
        Strick = sorted([Algorithm.S(x) for x in trick])
        Strongest = Strick[0]
        previous = Strongest
        counter = 0

        for i in range(1, 5):
            if Strick[i] == previous + 4:
                previous = Strick[i]
                counter += 1
            else:
                break
        if counter == 4:
            return "straight flush", Algorithm.inverseS(Strongest)
        
        CardRanks = [Algorithm.inverseS(x)[0] for x in Strick]
        if len(set(CardRanks)) == 2: # If only 2 ranks exist in the set, Its Fours' of Full House
            if 4 > CardRanks.count(CardRanks[0]) > 1:  # if its a Full House
                if CardRanks[2] != CardRanks[0]:   # Find determining (triplet) rank if its full house
                    return "full house", Algorithm.inverseS(Strick[4])
                else:
                    return "full house", Algorithm.inverseS(Strongest)

            else:  # Else we have Four of a kind
                if Algorithm.inverseS(Strick[1])[0] == Algorithm.inverseS(Strick[0])[0]:
                    return "four of a kind", Algorithm.inverseS(Strick[0])
                else:
                    return "four of a kind", Algorithm.inverseS(Strick[1])

        CardSuits = [Algorithm.inverseS(x)[1] for x in Strick]
        if len(set(CardSuits)) == 1:
            return "flush", Algorithm.inverseS(Strongest)
        else:
            return "straight", Algorithm.inverseS(Strongest)

    def is_stronger_trick(Algorithm, trick1_type, trick1_strongest, trick2_type, trick2_strongest, trick1, trick2):
        # Define the rankings of five-card trick types (lower rank means weaker trick)
        trick_rank = {
            'straight': 0,
            'flush': 1,
            'full house': 2,
            'four of a kind': 3,
            'straight flush': 4
        }


        # First, compare the trick types
        if trick_rank[trick1_type] > trick_rank[trick2_type]:
            return True
        elif trick_rank[trick1_type] < trick_rank[trick2_type]:
            return False

        if trick1 == 'flush':
            if Algorithm.check_stronger_flush(trick1, trick2):
                return True
            else:
                return False

        # Compare card values first
        if Algorithm.S(trick1_strongest) < Algorithm.S(trick2_strongest):
            return True
        else:
            return False




    def has_overlap(Algorithm, trick1, trick2):
        """Helper method to check if two tricks overlap (use the same cards)."""
        cards1 = set(trick1[-1])
        cards2 = set(trick2[-1])
        return not cards1.isdisjoint(cards2)

    def backtrack(Algorithm, tricks, start, current_arrangement, used_cards, total_cards):
        """Recursive backtracking method to find all valid arrangements."""
        # Base case: if all cards have been used, yield the arrangement
        if len(used_cards) == total_cards:
            yield current_arrangement[:]
            return

        for i in range(start, len(tricks)):
            trick = tricks[i]
            trick_cards = set(trick[-1])

            # If the current trick doesn't reuse cards, proceed with recursion
            if trick_cards.isdisjoint(used_cards):
                # Mark these cards as used and proceed to the next trick
                current_arrangement.append(trick)
                used_cards.update(trick_cards)

                # Recursively search for the next trick
                yield from Algorithm.backtrack(tricks, i + 1, current_arrangement, used_cards, total_cards)

                # Backtrack: remove the trick and unmark its cards
                current_arrangement.pop()
                used_cards.difference_update(trick_cards)

    def find_trick_arrangements(Algorithm, tricks, total_cards):
        """Public method that takes tricks as input and finds all valid arrangements."""
        return list(Algorithm.backtrack(tricks, 0, [], set(), total_cards))


    def score_trick(Algorithm, trick, copyofMyHand, deadCards, state: MatchState):
        """Score individual tricks based on the rules provided."""
        type_of_trick = trick[1]
        trick_cards = trick[-1]

        score = 0
        if type_of_trick == 'straight flush':
            score += SCORING['straight flush']
        elif type_of_trick == 'four of a kind + single':
            score += SCORING['four-of-a-kind']
        elif type_of_trick == 'full house':
            score += SCORING['full house']
        elif type_of_trick == 'flush':
            score += SCORING['flush']
        elif type_of_trick == 'straight':
            score += SCORING['straight']
        elif type_of_trick == 'triple':
            score += SCORING['triple']
        elif type_of_trick == 'pair':
            score += SCORING['pair']
            
        elif type_of_trick == 'single':
            # Get the Srel value of the card
            card_value = Algorithm.Srel(trick_cards[0], deadCards, copyofMyHand)
            score += Algorithm.single_card_points(trick_cards[0], deadCards, copyofMyHand)

        # Apply flexibility bonuses
        if type_of_trick == 'full house':
            score += 5
        elif type_of_trick == 'four of a kind + single':
            score += 3

        return score

    def score_arrangements(Algorithm, arrangements, copyofMyHand, deadCards, state: MatchState):
        """Score the entire arrangement and return them sorted by score."""
        scored_arrangements = []

        for arrangement in arrangements:
            total_score = 0
            trick_types = set()

            # Sum up scores for individual tricks
            for trick in arrangement:
                total_score += Algorithm.score_trick(trick, copyofMyHand, deadCards, state)
                trick_types.add(trick[1])

            # Apply diversity bonus for distinct combo types
            total_score += 2 * len(trick_types)

            scored_arrangements.append((arrangement, total_score))

        # Sort by score (descending order)
        scored_arrangements.sort(key=lambda x: x[1], reverse=True)

        return scored_arrangements

    def is_stronger_pair(Algorithm, pair1, pair2):
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
        
    def is_stronger_triple(Algorithm, triple1, triple2):
        determinant1 = triple1[0]
        if Algorithm.S(triple1[1]) < Algorithm.S(triple1[0]):
            determinant1 = triple1[1]
        if Algorithm.S(triple1[2]) < Algorithm.S(determinant1):
            determinant1 = triple1[2]

        determinant2 = triple2[0]
        if Algorithm.S(triple2[1]) < Algorithm.S(triple2[0]):
            determinant2 = triple2[1]

        if Algorithm.S(triple2[2]) < Algorithm.S(determinant1):
            determinant2 = triple2[2]

        if Algorithm.S(determinant1) < Algorithm.S(determinant2):
            return True
        else:
            return False


    def countRounds(Algorithm, gameHistory: List[List[Trick]]):
        singleRounds = 0
        pairRounds = 0
        TripleRounds = 0
        FiverRounds = 0
        for round in gameHistory:
            trickSize = len(round[0].cards)
            if trickSize == 1:
                singleRounds += 1
            elif trickSize == 2:
                pairRounds += 1
            elif trickSize == 3:
                TripleRounds += 1
            else:
                FiverRounds += 1
        return singleRounds, pairRounds, TripleRounds, FiverRounds
    
    def playerNumbers(Algorithm, state: MatchState):
        myPlayerNum = state.myPlayerNum  # Player numbers are 0 to 3
        PlayerAfterMe = (myPlayerNum + 1) % 4
        PlayerBeforeMe = (myPlayerNum + 3) % 4
        PlayerOppositeMe = (myPlayerNum + 2) % 4
        PlayersNotIncludingMe = [PlayerAfterMe, PlayerOppositeMe, PlayerBeforeMe]
        return myPlayerNum, PlayersNotIncludingMe

    def getAction(Algorithm, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration

        myPlayerNum, PlayersNotIncludingMe = Algorithm.playerNumbers(state)
        deadCards = Algorithm.countDeadCards(state.matchHistory[-1])

        singleRounds, pairRounds, tripleRounds, fiverRounds = Algorithm.countRounds(state.matchHistory[-1].gameHistory)
        endgame = False
        loss_aversion = False


        # TODO Write your algorithm logic here
        myHand = state.myHand
        myHand = Algorithm.sortCards(myHand)
        copyofMyHand = myHand.copy()
        #print("MY HAND")
        #print(myHand)



        toBeat = state.toBeat
        currentTrick = Algorithm.getCurrentTrickType(toBeat)

        # print("CURRENT TRICK")
        # print(currentTrick)
        
        allCombinations = Algorithm.getAllCombinations(myHand)
        valid_arrangements = Algorithm.find_trick_arrangements(allCombinations, len(myHand))
        #print("Random valid arrangement: ")
        #print(valid_arrangements[random.randint(0, len(valid_arrangements)-1)])

        scored_arrangements = Algorithm.score_arrangements(valid_arrangements, copyofMyHand, deadCards, state)
        
        #print("The top 3 arrangements: ")
        #print(" \n ")
        #print(scored_arrangements[0])
        #if len(scored_arrangements) > 3:
        #    print(" \n ")
        #    print(scored_arrangements[1])
        #    print(" \n ")
        #    print(scored_arrangements[2])

        singles = [trick[4] for trick in scored_arrangements[0][0] if trick[1] == 'single']
        pairs = [trick[4] for trick in scored_arrangements[0][0] if trick[1] == 'pair']
        triples = [trick[4] for trick in scored_arrangements[0][0] if trick[1] == 'triple']
        fives = [trick[4] for trick in scored_arrangements[0][0] if trick[1] != 'triple' and trick[1] != 'pair' and trick[1] != 'single']
       
        strategy = singles + pairs + triples + fives    


        print(f"strategy : {strategy}")
        mustBeForced = []
        controlCards = []
        if len(singles) > 0:
            for i in range(len(singles)):
                if Algorithm.Srel(singles[i][0], deadCards, copyofMyHand) == 0:
                    controlCards.append(singles[i])
                elif Algorithm.Srel(singles[i][0], deadCards, copyofMyHand) >= (39 - len(deadCards) - 4):
                    mustBeForced.append(singles[i])

        if len(pairs) > 0:
            #print(f"My first pair has S value of [stronger, weaker] {Algorithm.SrelTrick(pairs[0], deadCards, copyofMyHand)}")
            #cardsInGame = [Algorithm.inverseS(s) for s in range(51) if Algorithm.inverseS(s) not in deadCards and Algorithm.inverseS(s) not in copyofMyHand]
            #print_cards_matrix_debug(cardsInGame)
            for i in range(len(pairs)):
                if Algorithm.SrelTrick(pairs[i], deadCards, copyofMyHand)[0] <= 1:
                    controlCards.append(pairs[i])
                elif Algorithm.SrelTrick(pairs[i], deadCards, copyofMyHand)[1] < 3:
                    mustBeForced.append(pairs[i])
            

        if len(triples) > 0:
            #print(f"My first triple has S value of [stronger, weaker] {Algorithm.SrelTrick(triples[0], deadCards, copyofMyHand)}")
            for i in range(len(triples)):
                if Algorithm.SrelTrick(triples[i], deadCards, copyofMyHand)[1] <= 2:
                    controlCards.append(triples[i])
                elif Algorithm.SrelTrick(triples[i], deadCards, copyofMyHand)[0] <= 2:
                    mustBeForced.append(triples[i])

        print(f"These tricks are so weak they must be forced: {mustBeForced}")
        print(f"These tricks are most likely control cards: {controlCards}")

        if len(strategy) <= 3:
            endgame = True
            print("entering endgame")

        for playerNum in PlayersNotIncludingMe:
            if state.players[playerNum].handSize < 3:
                loss_aversion = True
                print(f"ENTERING Loss aversion mode, player {playerNum} has {state.players[playerNum].handSize} cards left")

        
        #for single in singles:
        #    print(f"There is {Algorithm.Srel(single[0], deadCards, copyofMyHand)} stronger singles than {single} in game \n")
        #if endgame is False:
        if '3D' in myHand:
            for trick in strategy:
                if '3D' in trick:
                    action = trick
        
        elif state.toBeat is None:
            # Play weakest high order trick
            for trick in strategy:
                if len(fives) > 0:
                    action = strategy[-len(fives)]
                elif len(triples) > 0:
                    action = strategy[-len(triples)]
                elif len(pairs) > 0:
                    action = strategy[-len(pairs)]
                else:
                    if loss_aversion is True:
                        action = strategy[-1]
                    else:
                        action = strategy[0]
        
        elif len(state.toBeat.cards) == 1:
            print(f"This is the {singleRounds} singles round")
            StoBeat = Algorithm.S(state.toBeat.cards[0])
            if loss_aversion is False:
                for i in range(len(singles)):
                    if Algorithm.S(strategy[i][0]) < StoBeat:
                        action = strategy[i]
                        break
            else:
                if Algorithm.S(copyofMyHand[-1]) < StoBeat: # PLay strongest card if I can
                    action.append(copyofMyHand[-1])

        elif len(state.toBeat.cards) == 2:
            for i in range(len(singles),len(singles) + len(pairs)):
                if Algorithm.is_stronger_pair(strategy[i], state.toBeat.cards):
                    action = strategy[i]
                    break

        elif len(state.toBeat.cards) == 3:
            for i in range(len(singles) + len(pairs), len(singles) + len(pairs) + len(triples)):
                if Algorithm.is_stronger_triple(strategy[i], state.toBeat.cards):
                    action = strategy[i]
                    break                

        elif len(state.toBeat.cards) == 5:
            if len(fives) > 0:
                trickType, determinant = Algorithm.TypeOfFiveCardTrick(state.toBeat.cards)
                for i in range(len(fives)):
                    print
                    challengerTrickType, challengerDeterminant = Algorithm.TypeOfFiveCardTrick(strategy[-1-i])
                    if Algorithm.is_stronger_trick(challengerTrickType, challengerDeterminant, trickType, determinant, state.toBeat.cards, Algorithm.TypeOfFiveCardTrick(strategy[-1-i])):
                        action = strategy[-i-1]
                        break
        #else: # End Game operation
        #    if len(strategy) == 3:
        #        action = strategy[1]

        #    elif len(strategy) == 2:
        #        action = strategy[1]
        #    else:
        #        action = strategy[0]

        return action, myData