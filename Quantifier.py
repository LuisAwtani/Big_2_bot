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
        # Compute which stronger pairs are still in the game 
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
    

    def cardsHeldByPlayer(self, PlayerNum: int, Players: List[Player]):
        cardsHeld = Players[PlayerNum].handSize
        return cardsHeld


    def tricksPlayedByPlayer(self, state: MatchState, PlayerNum: int):
        tricks = []
        for GameHistory in state.matchHistory:
            if GameHistory.finished is False: # If this is the correct (current) game beign played
                for round in GameHistory.gameHistory:
                    for trick in round:
                        if trick.playerNum == PlayerNum:
                            tricks.append(trick.cards)
        return tricks


    # For every card, what is the prob each player is holding that card
    def gameStartCardProbabilityDistribution(self, state: MatchState, DeadCards: set):
        notConsidered = []
        for deadCard in DeadCards:
            notConsidered.append(self.S(deadCard))

        for card in state.myHand:
            notConsidered.append(self.S(card))

        dist = []
        ScardsInPlay = [num for num in range(52) if num not in notConsidered]
        CardsInPlayQuantity = len(ScardsInPlay)
        for Scard in ScardsInPlay: 
            for playerNum in range(4):
                if playerNum != state.myPlayerNum:
                    probabilityVar = state.players[playerNum].handSize / CardsInPlayQuantity
                    dist.append([playerNum, Scard, probabilityVar])

        print(f"My player number is {state.myPlayerNum}")
        print("Probability distibution: (first 10)")
        for x in range(10):
            print(f"Player num: {dist[x][0]}, card: {self.inverseS(dist[x][1])}, prob: {dist[x][2]} \n")

        return dist




    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        deadCards = self.countDeadCards(state.matchHistory[-1])
        myData = state.myData   # Communications from the previous iteration
        myPlayerNum = state.myPlayerNum  # Player numbers are 0 to 3
        if myPlayerNum == 4:
            PlayerAfterMe = 0
        else:
            PlayerAfterMe = myPlayerNum + 1
        print(f"Player after me has played: {self.tricksPlayedByPlayer(state, PlayerAfterMe)}")
        
        #self.gameStartCardProbabilityDistribution(state, deadCards)
        #print(f"My player number is: {myPlayerNum}")
        MyCardQuantity = self.cardsHeldByPlayer(myPlayerNum, state.players)
        #print(f"I am holding {MyCardQuantity} cards")

        #print(f"Dead Cards are: {deadCards}")
        ### Sort hand from lowest to highest card
        sortedHand = sorted(state.myHand, key = lambda x : self.S(x), reverse=True) 

        #for x in sortedHand:
        #    if self.Srel(x,deadCards, sortedHand) == 0:
        #        print(f"I'm holding the strongest card in the game!: {x}")


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