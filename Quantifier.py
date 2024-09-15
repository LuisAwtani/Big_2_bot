from classes import *

class Algorithm:

    # Calculates the relative strength of a single card as a number to be used with Python's key comparison mechanism
    def S(self, Card: str):
        ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
        suits = ['S', 'H', 'C', 'D']
        rating = ranks.index(Card[0]) * 4 + suits.index(Card[1])
        return rating

    def countDeadCards(self, state: GameHistory):
        ThisGame = state.gameHistory
        deadCards = set()
        for x in ThisGame:
            for y in x:
                for card in y.cards:
                    deadCards.add(card)
        return deadCards

    def Srel(self, Card: str, deadCards, myHand):
        Sval = self.S(Card)
        for deadCard in deadCards:
            if self.S(deadCard) < Sval:
                Sval -= 1
        Hand = myHand.sorted(reverse=True)
        Hand.remove(Card)
        for x in Hand:
            if self.S(x) < self.S(Card):
                Sval
        return Sval


    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        deadCards = self.countDeadCards(state.matchHistory[-1])
        myData = state.myData   # Communications from the previous iteration


        print(f"Dead Cards are: {deadCards}")
        # Sort hand from lowest to highest card
        sortedHand = sorted(state.myHand, key = lambda x : self.S(x), reverse=True) 

        for x in sortedHand:
            if self.Srel(x,deadCards) == 0:
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

        # If the trick size is 2, 3, or 5, I will pass

        return action, myData