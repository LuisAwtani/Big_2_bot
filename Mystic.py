# Currently working Flag: ON
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

        Queue = []
        # Look for pairs 
        ## NOTE: Currently producing suboptimal pairs: change logic later
        pairlist = [[0, -1] for _ in range(13)]  # tracks [quantity, card] Index of cards in order of 2, K, Q, ..., 3
        for Scard in Ssingles:
            idx = Scard // 4
            pairlist[idx][0] += 1
            print(f"Found a {Scard} with index {idx}. \n pairlist is now {pairlist}")
            
            if pairlist[idx][0] == 2: # If we got a pair, find S value of twin, and move both to Queue
                if Scard < pairlist[idx][1]:
                    Queue.append((Scard, pairlist[idx][1]))
                else:
                    Queue.append((pairlist[idx][1], Scard))
            pairlist[idx][1] = Scard

        # Move cards in Queue out of single list (to avoid loop iteration bug in earlier loop)
        for x in Queue:
            print(f"Trying to remove: {x} from singles: {Ssingles}")
            Ssingles.remove(x[0])
            Ssingles.remove(x[1])
            if x[0] < x[1]:
                Spairs.append(x)
            else:
                Spairs.append((x[1], x[0]))
        
        # remaining cards are singles
        # Convert S values back to card strings
        singles = []
        for Sval in Ssingles:
            singles.append(self.inverseS(Sval))
        
        pairs = []
        for SvalTuple in Spairs:
            card1 = self.inverseS(SvalTuple[0])
            card2 = self.inverseS(SvalTuple[1])
            if self.S(card1) > self.S(card2):
                pairs.append((card1, card2))
            else:
                pairs.append((card2, card1))

        
        print(f"Pairs found: {pairs}, remaining single cards: {singles}")
        # Returns tricks as a tuple with most powerful card FIRST
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


        # If I start game or past 3 players have passed
        if state.toBeat is None:

            if len(pairs) > 0: # If we can play a pair trick, play weakest
                weakest = 52
                for x in pairs:
                    if self.S(x[0]) < weakest:
                        action = [x[0], x[1]]
                        weakest = self.S(x[0])
        
            elif len(singles) > 0:    #else play (second weakest) single card
                weakest = 52
                for x in singles:
                    if self.S(x) < weakest:
                        weakest = self.S(x)
                        action = [x]


        # If the trick size is 1, play second weakest card
        elif len(state.toBeat.cards) == 1:

            if True:     # TODO: IF we want to play, play second weakest card (rn just if true)
                choices = []
                cardToBeat = state.toBeat.cards[0]
                for card in singles: 
                    if self.S(card) < self.S(cardToBeat): # lower S value is stronger
                        choices.append(self.S(card))
                
                choices.sort()
                if len(choices) > 2:
                    action.append(self.inverseS(choices[-2])) # Play second weakest card
                elif len(choices) != 0:
                    action.append(self.inverseS(choices[-1])) ## PLay weakest card, update when 
        # If trick size is 2, try to play a pair              ## relative S function exists
        elif len(state.toBeat.cards) == 2:
            if len(pairs) > 0:
                weakest = min(self.S(x) for x in state.toBeat.cards)
                print(f"Cards to beat: {state.toBeat.cards}") 
                for x in pairs:
                    if self.S(x[0]) < weakest: #PLay weakest eligible pair
                        weakest = self.S(x[0])
                        action = [x[0], x[1]]   
                    
    
        # If the trick size is 2, 3, or 5, I will pass

        #NOTE: action must be a list of strings
        return action, myData