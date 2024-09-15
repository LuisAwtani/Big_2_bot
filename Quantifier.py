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
                    pairs.append((hand[i], hand[j]))
                else:
                    break
        return pairs

    def SrelPairs(self, Pair: tuple, deadCards, myHand):
        # Compute which stronger cards are still in the game 
        Sval = self.S(Pair[0])
        inPlay = []
        if Sval > 49:   # Prevents overshoot when we check pairs for 3
            Sval = 49
        for s in range(Sval+2, -1, -1): # Start indexing 2 cards weaker (4H,4C is weaker than 4S,4D)
            Card = self.inverseS(s)
            if Card not in deadCards:
                if Card not in myHand:  # Don't consider cards that you're holding
                    inPlay.append(Card)
        strongerpairs = self.findPairs(inPlay)        
        return strongerpairs



    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        deadCards = self.countDeadCards(state.matchHistory[-1])
        myData = state.myData   # Communications from the previous iteration


        #print(f"Dead Cards are: {deadCards}")
        # Sort hand from lowest to highest card
        sortedHand = sorted(state.myHand, key = lambda x : self.S(x), reverse=True) 

        for x in sortedHand:
            if self.Srel(x,deadCards, sortedHand) == 0:
                print(f"I'm holding the strongest card in the game!: {x}")


        # If I am the first to play, play my weakest one card trick
        if state.toBeat is None: 
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
            print(f"S value to beat: {StoBeat} which is card {self.inverseS(StoBeat)}")
            if len(pairs) > 0:
                for pair in pairs:
                    if self.S(pair[0]) < StoBeat:
                        action = [pair[0], pair[1]]
                        print(f"S value im tryna play: {self.S(pair[0])} which is card {pair[0]}")
                        strongerPairs = self.SrelPairs(pair, deadCards, sortedHand)
                        print(f"Stronger pairs ingame than the one i'm trying to play: {strongerPairs}")

            

        # If the trick size is 2, 3, or 5, I will pass

        return action, myData