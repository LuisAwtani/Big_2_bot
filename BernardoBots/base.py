from classes import *
from collections import defaultdict
from itertools import combinations, product
import random

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

    def Srel(Algorithm, Card: str, deadCards: set, copyofMyHand: list):
        Sval = Algorithm.S(Card)
        for deadCard in deadCards:
            if Algorithm.S(deadCard) < Sval:
                Sval -= 1

        Hand = sorted(copyofMyHand, reverse=True)
        Hand.remove(Card)
        for x in Hand:
            if Algorithm.S(x) < Algorithm.S(Card):
                Sval
        return Sval
    
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

    def is_stronger_trick(Algorithm, trick1_type, trick1_strongest, trick2_type, trick2_strongest):
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

        # If trick types are the same, compare the strongest cards
        trick1_value, trick1_suit = trick1_strongest[:-1], trick1_strongest[-1]
        trick2_value, trick2_suit = trick2_strongest[:-1], trick2_strongest[-1]

        # Compare card values first
        if Algorithm.S([trick1_value]) < Algorithm.S([trick2_value]):
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


    def score_trick(Algorithm, trick, copyofMyHand, deadCards):
        """Score individual tricks based on the rules provided."""
        type_of_trick = trick[1]
        trick_cards = trick[-1]

        score = 0
        if type_of_trick == 'straight flush':
            score += 55
        elif type_of_trick == 'four of a kind + single':
            score += 50
        elif type_of_trick == 'full house':
            score += 45
        elif type_of_trick == 'flush':
            score += 35
        elif type_of_trick == 'straight':
            score += 30
        elif type_of_trick == 'triple':
            score += 25
        elif type_of_trick == 'pair':
            score += 15
        elif type_of_trick == 'single':
            # Get the Srel value of the card
            card_value = Algorithm.Srel(trick_cards[0], deadCards, copyofMyHand)
            if 0 <= card_value < 3:
                score += 20
            elif 3 <= card_value <= 7:
                score += 10
            else:
                score += 1
            if card_value == 0:
                score += 10  # Bonus for guaranteed control

        # Apply flexibility bonuses
        if type_of_trick == 'full house':
            score += 5
        elif type_of_trick == 'four of a kind + single':
            score += 3

        return score

    def score_arrangements(Algorithm, arrangements, copyofMyHand, deadCards):
        """Score the entire arrangement and return them sorted by score."""
        scored_arrangements = []

        for arrangement in arrangements:
            total_score = 0
            trick_types = set()

            # Sum up scores for individual tricks
            for trick in arrangement:
                total_score += Algorithm.score_trick(trick, copyofMyHand, deadCards)
                trick_types.add(trick[1])

            # Apply diversity bonus for distinct combo types
            total_score += 2 * len(trick_types)

            scored_arrangements.append((arrangement, total_score))

        # Sort by score (descending order)
        scored_arrangements.sort(key=lambda x: x[1], reverse=True)

        return scored_arrangements



    def getAction(Algorithm, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration
        deadCards = Algorithm.countDeadCards(state.matchHistory[-1])

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

        scored_arrangements = Algorithm.score_arrangements(valid_arrangements, copyofMyHand, deadCards)
        
        print("Top 3 arrangements: ")
        print(" \n ")
        print(scored_arrangements[0])
        print(" \n ")
        #print(scored_arrangements[1])
        #print(" \n ")
        #print(scored_arrangements[2])

        singles = [trick[4] for trick in scored_arrangements[0][0] if trick[1] == 'single']
        pairs = [trick[4] for trick in scored_arrangements[0][0] if trick[1] == 'pair']
        triples = [trick[4] for trick in scored_arrangements[0][0] if trick[1] == 'triple']
        fives = [trick[4] for trick in scored_arrangements[0][0] if trick[1] != 'triple' and trick[1] != 'pair' and trick[1] != 'single']
       
        strategy = singles + pairs + triples + fives    
            
        print(f"strategy : {strategy}")
        

        if '3D' in myHand == 0:
            for trick in strategy:
                if '3D' in trick:
                    action = trick

        elif len(toBeat) == 0:
            for trick in strategy:
                if len(fives) > 0:
                    action = strategy[-len(fives)]
                elif len(triples) > 0:
                    action = strategy[-len(triples)]
                elif len(pairs) > 0:
                    action = strategy[-len(pairs)]
                else:
                    action = strategy[0]
        
        elif len(toBeat) == 1:
            StoBeat = Algorithm.S(toBeat[0])
            for i in range(len(singles)):
                if Algorithm.S(strategy[i][0]) < StoBeat:
                    action = strategy[i]
                    break

        elif len(toBeat) == 5:
            if len(fives) > 0:
                trickType, determinant = Algorithm.TypeOfFiveCardTrick(toBeat)
                for i in range(len(fives)):
                    challengerTrickType, challengerDeterminant = Algorithm.TypeOfFiveCardTrick(strategy[-i])
                    if Algorithm.is_stronger_trick(challengerTrickType, challengerDeterminant, trickType, determinant):
                        action = strategy[-i]
                        break
            
        return action, myData