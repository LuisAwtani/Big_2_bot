# Hello World (Sorry this is taking me forever)
from classes import *

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


    #def relativeS(self, S):
    # TODO: function that evaluates relative value of S



    def make_strategy(self, handInput):

        # initially, all cards are single
        Ssingles = handInput # hand input is in S values, NOT strings
        Spairs = []

        # Scan hand tricks, return combination with fewest singles NOTE: Currently only returns singles and pairs
        changes = 1
        while (changes > 0): # until 0 tricks found
            changes = 0

            # Look for pairs
            pairlist = [0] * 13  # tracks quantity, Index of cards in order of 2, K, Q, ..., 3
            for Scard in Ssingles:
                idx = Scard // 4
                pairlist[idx] += 1
                if pairlist[idx] == 2: # If we got a pair, find S value of twin, and move both from singles to pairs
                    changes += 1
                    for Stwin in Ssingles: 
                        if (Stwin // 4) == (Scard // 4):
                            Ssingles.remove(Scard)
                            Ssingles.remove(Stwin)
                            Spairs.append((Scard, Stwin)) # Append pair as a tuple

        # Convert S values back to card strings
        singles = []
        for Sval in Ssingles:
            singles.append(self.inverseS(Sval))
        
        pairs = []
        for SvalTuple in Spairs:
            card1 = self.inverseS(SvalTuple[0])
            card2 = self.inverseS(SvalTuple[1])
            pairs.append((card1, card2))
        return [singles, pairs]



    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        myData = state.myData   # Communications from the previous iteration

        # Sort hand from lowest to highest S
        sortedHand = sorted(state.myHand, key = lambda x : self.S(x)) 
        sValSortedHand = sorted([self.S(card) for card in sortedHand])

        # strategy will be a list of [singles, pairs] as strings (INCOMPLETE must include all trick types)
        strategy = self.make_strategy(sValSortedHand) 
        singles = strategy[0]
        pairs = strategy[1]


        # If I am the first to play, play 3 of Diamonds
        if state.toBeat is None:

            # NOTE: Bug if all for 3s in pairs, however, this should never happen
            if sortedHand[-1] in pairs:    # if 3 is in a pair, append that pair
                for pair in pairs:
                    if pair[0].startswith('3'):
                        action.append(pair[0])
                        action.append(pair[1])
            else: # 3 is a solo card
                action.append(sortedHand[-1]) # Play 3 of Diamonds


        # If the trick size is 1, play second weakest card
        elif len(state.toBeat.cards) == 1:

            if True:     # TODO: IF we want to play, play second weakest card (rn just if true)
                choices = []
                cardToBeat = state.toBeat.cards[0]
                for card in singles: 
                    if self.S(card) > self.S(cardToBeat):
                        choices.append(self.S(card))
                if len(choices) > 1:
                    choices.sort()
                    action.append(self.inverseS(choices[1]))


        # If trick size is 2, try to play a pair
        elif len(state.toBeat.cards) == 2:
            if len(pairs) > 0:
                action.append(pairs[0])
  


        # If the trick size is 2, 3, or 5, I will pass
        return action, myData