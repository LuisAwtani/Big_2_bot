from classes import *
from math import factorial
from collections import defaultdict
from itertools import combinations, product
rank_order = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
suit_order = {'D': 0, 'C': 1, 'H': 2, 'S': 3}

class Algorithm:

    # Calculates the relative strength of a single card as a number to be used with Python's key comparison mechanism
    def S(self, Card: str):
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

    def countDeadCards(self, state: GameHistory):
        ThisGame = state.gameHistory
        deadCards = set()
        for x in ThisGame:
            for y in x:
                for card in y.cards:
                    deadCards.add(card)
        return deadCards

    def Srel(self, Card: str, deadCards: set, myHand: list):
        Sval = self.S(Card)
        for deadCard in deadCards:
            if self.S(deadCard) < Sval:
                Sval -= 1
        Hand = sorted(myHand, reverse=True)
        Hand.remove(Card)
        for x in Hand:
            if self.S(x) < self.S(Card):
                Sval
        return Sval

    def findPairs(self, hand):
        pairs = []
        for i in range(0, len(hand)):
            for j in range(i + 1, len(hand)):
                if hand[i][0] == hand[j][0]:
                    if self.S(hand[i]) > self.S(hand[j]):
                        pairs.append((hand[i], hand[j]))
                    else:
                        pairs.append((hand[j], hand[i]))
                else:
                    break
        return pairs
    

    def StrongerPairs(self, Pair: tuple, deadCards, myHand):
        # Compute which stronger pairs are still in the game 
        Sval = self.S(Pair[0])
        inPlay = []
        if Sval > 49:   # Prevents overshoot when we check pairs for 3
            Sval = 49
        if Sval % 4 == 0:
            indexer = Sval - 1   # Prevents Checking for same rank pairs when a Spade is played
        else:
            indexer = Sval + 2
        for s in range(indexer, -1, -1): # Start indexing 2 cards weaker (3H,3C is weaker than 3S,3D)
            Card = self.inverseS(s)
            if Card not in deadCards:
                if Card not in myHand:  # Don't consider cards that you're holding
                    inPlay.append(Card)
        strongerpairs = self.findPairs(inPlay)        
        return strongerpairs
    
    # Function returns type of five card trick (string) along with strongest (determinant) card
    def TypeOfFiveCardTrick(self, trick: list):
        Strick = sorted([self.S(x) for x in trick])
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
            return "straight flush", self.inverseS(Strongest)
        
        CardRanks = [self.inverseS(x)[0] for x in Strick]
        if len(set(CardRanks)) == 2: # If only 2 ranks exist in the set, Its Fours' of Full House
            if 4 > CardRanks.count(CardRanks[0]) > 1:  # if its a Full House
                if CardRanks[2] != CardRanks[0]:   # Find determining (triplet) rank if its full house
                    return "full house", self.inverseS(Strick[4])
                else:
                    return "full house", self.inverseS(Strongest)

            else:  # Else we have Four of a kind
                if self.inverseS(Strick[1])[0] == self.inverseS(Strick[0])[0]:
                    return "four of a kind", self.inverseS(Strick[0])
                else:
                    return "four of a kind", self.inverseS(Strick[1])

        CardSuits = [self.inverseS(x)[1] for x in Strick]
        if len(set(CardSuits)) == 1:
            return "flush", self.inverseS(Strongest)
        else:
            return "straight", self.inverseS(Strongest)
        

    def cardsHeldByPlayer(self, PlayerNum: int, Players: List[Player]):
        cardsHeld = Players[PlayerNum].handSize
        return cardsHeld


    def tricksPlayedByPlayer(self, state: MatchState, PlayerNum: int):
        tricks = []
        GameHistory = state.matchHistory[-1]

        for round in GameHistory.gameHistory:
            toBeat = ['Start']
            for trick in round:
                if trick.playerNum == PlayerNum:
                    tricks.append((toBeat, trick.cards))
                if len(trick.cards) > 0:
                    toBeat = trick.cards
        return tricks

    # x is total cards in the game, y is the way those cards may be arranged (y < x)
    def PossibleArrangements(self, x: int, y: int):
        return factorial(x) // (factorial(x-y) * factorial(y))


    def tracePlayerProbabilityStatements(self, state: MatchState, Player: int):
        PlayerHandSize = state.players[Player].handSize
        noResponseFives = []
        playersHistory = self.tricksPlayedByPlayer(state, Player)
        #print(f"playersHistory variable is: {playersHistory}")

        lowestUnansweredSingle = ['2S', False]  # Card, beaten flag pair
        #### Remembers the lowest single card the player didn't answer,
        #### If player plays a single higher card (one that could have beaten the earlier 
        #### card), raises the beaten flag

        print(f"Investigating PLayer {Player}'s History")
        for play in playersHistory:
            toBeat = play[0]
            Response = play[1]
            
            if toBeat[0] == 'Start':
                print(f"Player {Player} decided to start round with {Response}")
                if len(Response) == 1:
                    if self.S(Response[0]) < self.S(lowestUnansweredSingle[0]) and state.players[Player].handSize > 3:
                        # Checks If the card would hv beaten earlier unanswered single card
                        lowestUnansweredSingle[1] = True
                        #print(f"I think {Response[0]} used to belong to a higher order trick!")

            elif len(toBeat) == 5:
                if not Response:
                    trickType, determinantCard = self.TypeOfFiveCardTrick(toBeat)
                    noResponseFives.append((trickType, determinantCard, PlayerHandSize))
                    #print(f"Player {Player} did not respond to a {trickType} of order {determinantCard}!")

            #elif len(toBeat) == 3:
                #if not Response:
                    #print(f"Player {Player} did not respond to a triple of rank {toBeat[0]}!")
   
            #elif len(toBeat) == 2:
                #if not Response:
                    #print(f"Player {Player} did not Respond to Pair {toBeat}")

            elif len(toBeat) == 1:
                if not Response:
                    #print(f"Player {Player} did not Respond to 1 card trick: {toBeat[0]}")
                    if self.S(toBeat[0]) > self.S(lowestUnansweredSingle[0]):
                        lowestUnansweredSingle[0] = toBeat[0]
                    
                else: #if player responded, check the flag
                    if self.S(Response[0]) < self.S(lowestUnansweredSingle[0]) and state.players[Player].handSize > 3:
                         # Checks If the card would hv beaten earlier unanswered single card
                        lowestUnansweredSingle[1] = True
                        #print(f"I think {Response[0]} used to belong to a higher order trick!")
        return noResponseFives, lowestUnansweredSingle


    # Helper functions to check various trick types
    def is_flush(self, hand):
        suits = [card[1] for card in hand]
        return len(set(suits)) == 1

    def is_straight(self, hand):
        hand_ranks = sorted([rank_order.index(card[0]) for card in hand])
        for i in range(len(hand_ranks) - 4):
            if hand_ranks[i:i+5] == list(range(hand_ranks[i], hand_ranks[i]+5)):
                return True
        return False

    def is_full_house(self, hand):
        rank_count = {}
        for card in hand:
            rank = card[0]
            rank_count[rank] = rank_count.get(rank, 0) + 1
        return 3 in rank_count.values() and 2 in rank_count.values()

    def is_four_of_a_kind(self, hand):
        rank_count = {}
        for card in hand:
            rank = card[0]
            rank_count[rank] = rank_count.get(rank, 0) + 1
        return 4 in rank_count.values()

    def is_straight_flush(self, hand):
        return self.is_straight(hand) and self.is_flush(hand)

    def strongest_card(self, hand):
        """Finds the strongest card in a hand based on the S value."""
        return min(hand, key=self.S)

    def compare_hands(self, hand1, hand2):
        """
        Compare two hands based on their strongest cards using the S function.
        Returns True if hand1 is weaker than hand2 (i.e., has higher S value), False otherwise.
        """
        return self.S(self.strongest_card(hand1)) < self.S(self.strongest_card(hand2))


    def MakeTableBasedonDisprovenHands(self, cards, trick_type, strongest_card_of_trick, hand_size, playerNum):
        """
        Outputs a list of lists, where each sublist is a hand we've disproven
        (i.e., hands that form a flush, straight, full house, straight flush, or four of a kind),
        with the strongest card at the 0th index.
        
        Parameters:
        cards (list): The remaining cards in game among the other players.
        trick_type (str): The type of 5-card trick being compared (flush, straight, full house, etc.).
        strongest_card_of_trick (str): The strongest card of the already played trick.
        hand_size (int): The number of cards the player holds.
        
        Returns:
        list: A list of hands (disproven hands) that form the same or stronger type of trick but are weaker than the input trick.
        """
        all_k_card_combinations = list(combinations(cards, hand_size))  # Generate all hand_size-card combinations
        disproven_hands = []
        
        # Iterate through all possible k-card hands
        for hand in all_k_card_combinations:
            hand = list(hand)
            valid_5_card_tricks = []

            # Evaluate all 5-card subsets of this k-sized hand
            for five_card_subset in combinations(hand, 5):
                five_card_subset = list(five_card_subset)

                # Handle each trick type in descending strength order
                if trick_type == 'straight flush' and self.is_straight_flush(five_card_subset):
                    if self.compare_hands(five_card_subset, [strongest_card_of_trick]):
                        valid_5_card_tricks.append(five_card_subset)
                elif trick_type == 'four of a kind':
                    if self.is_four_of_a_kind(five_card_subset):
                        if self.compare_hands(five_card_subset, [strongest_card_of_trick]):
                            valid_5_card_tricks.append(five_card_subset)
                    elif self.is_straight_flush(five_card_subset):  # Stronger than four of a kind, automatically add
                        valid_5_card_tricks.append(five_card_subset)
                elif trick_type == 'full house':
                    if self.is_full_house(five_card_subset):
                        if self.compare_hands(five_card_subset, [strongest_card_of_trick]):
                            valid_5_card_tricks.append(five_card_subset)
                    elif self.is_four_of_a_kind(five_card_subset) or self.is_straight_flush(five_card_subset):
                        valid_5_card_tricks.append(five_card_subset)
                elif trick_type == 'flush':
                    if self.is_flush(five_card_subset):
                        if self.compare_hands(five_card_subset, [strongest_card_of_trick]):
                            valid_5_card_tricks.append(five_card_subset)
                    elif self.is_full_house(five_card_subset) or self.is_four_of_a_kind(five_card_subset) or self.is_straight_flush(five_card_subset):
                        valid_5_card_tricks.append(five_card_subset)
                elif trick_type == 'straight':
                    if self.is_straight(five_card_subset):
                        if self.compare_hands(five_card_subset, [strongest_card_of_trick]):
                            valid_5_card_tricks.append(five_card_subset)
                    elif self.is_flush(five_card_subset) or self.is_full_house(five_card_subset) or self.is_four_of_a_kind(five_card_subset) or self.is_straight_flush(five_card_subset):
                        valid_5_card_tricks.append(five_card_subset)

            # If valid tricks were found, add the k-sized hand
            if valid_5_card_tricks:
                strongest_trick = min(valid_5_card_tricks, key=lambda hand: self.S(self.strongest_card(hand)))  # Pick strongest 5-card trick
                hand_sorted = sorted(hand, key=self.S)  # Sort entire k-sized hand by strength (S value)
                disproven_hands.append(hand_sorted)

        table = self.tableGenerator(playerNum, disproven_hands, cards, hand_size)
        return table


    def tableGenerator(self, playerNum: int, disprovenHands: list, cardsInPlay: list, playerHandSize):
        prb1 = self.PossibleArrangements(len(cardsInPlay), playerHandSize)
        prb2 = self.PossibleArrangements(len(cardsInPlay)-1, playerHandSize-1) 
        totalDisprovenScenarios = len(disprovenHands)
        table = []
        disprovenList = [0 for _ in range(52)]
        for hand in disprovenHands:
            for card in hand:
                disprovenList[self.S(card)] += 1

        for card in cardsInPlay:
            table.append((playerNum, card, (prb2 - disprovenList[self.S(card)]) / (prb1 - totalDisprovenScenarios)))
        return table



    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        deadCards = self.countDeadCards(state.matchHistory[-1])
        myData = state.myData   # Communications from the previous iteration
        myPlayerNum = state.myPlayerNum  # Player numbers are 0 to 3
        PlayerAfterMe = (myPlayerNum + 1) % 4
        PlayerBeforeMe = (myPlayerNum + 3) % 4
        PlayerOppositeMe = (myPlayerNum + 2) % 4
        PlayersNotIncludingMe = [PlayerAfterMe, PlayerOppositeMe, PlayerBeforeMe]

        statements = self.tracePlayerProbabilityStatements(state, PlayerAfterMe)
        print(statements)


        sortedHand = sorted(state.myHand, key = lambda x : self.S(x), reverse=True) 
        # If I am the first to play, play my weakest one card trick
        if len(deadCards) == 0: 
            action.append(sortedHand[0])

        elif state.toBeat is None:
            action.append(sortedHand[0])

        # If the trick size is 1, play my weakest trick that still beats this one, or pass nothing otherwise
        elif len(state.toBeat.cards) == 1:
            cardToBeat = state.toBeat.cards[0]
            for card in sortedHand:
                if self.S(card) < self.S(cardToBeat):
                    action.append(card)
                    break

        elif len(state.toBeat.cards) == 2:
            StoBeat = min([self.S(card) for card in state.toBeat.cards])
            pairs = self.findPairs(sortedHand)
            #print(f"S value to beat: {StoBeat} which is card {self.inverseS(StoBeat)}")
            if len(pairs) > 0:
                for pair in pairs:  # Weakest pair should be at the end
                    if self.S(pair[0]) < StoBeat:
                        action = [pair[0], pair[1]]
                if action:
                    pair = (action[0], action[1])
                    #print(f"S value im trying to play: {self.S(pair[0])} which is card {pair[0]}")
                    strongerPairs = self.StrongerPairs(pair, deadCards, sortedHand)
                    #print(f"Stronger pairs ingame than the one i'm trying to play: {strongerPairs}")


            

        # If the trick size is 2, 3, or 5, I will pass

        return action, myData