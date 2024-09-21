from classes import *
from math import factorial
FiveCardTrickPriorityOrder = {'Straight Flush': 0, 'FourOfaKind': 1, 'FullHouse': 2, 'Flush': 3, 'Straight': 4}


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
            return "StraightFlush", self.inverseS(Strongest)
        
        CardRanks = [self.inverseS(x)[0] for x in Strick]
        if len(set(CardRanks)) == 2: # If only 2 ranks exist in the set, Its Fours' of Full House
            if 4 > CardRanks.count(CardRanks[0]) > 1:  # if its a Full House
                if CardRanks[2] != CardRanks[0]:   # Find determining (triplet) rank if its full house
                    return "FullHouse", self.inverseS(Strick[4])
                else:
                    return "FullHouse", self.inverseS(Strongest)

            else:  # Else we have Four of a kind
                if self.inverseS(Strick[1])[0] == self.inverseS(Strick[0])[0]:
                    return "FourOfaKind", self.inverseS(Strick[0])
                else:
                    return "FourOfaKind", self.inverseS(Strick[1])

        CardSuits = [self.inverseS(x)[1] for x in Strick]
        if len(set(CardSuits)) == 1:
            return "Flush", self.inverseS(Strongest)
        else:
            return "Straight", self.inverseS(Strongest)
        





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


    # Function estimates probability of PLAYER x holding CARD y
    def ChancePlayerHoldsCertainCard(self, state: MatchState, Player: int, Scard: int, SnotConsidered: list):
        PlayerHandSize = state.players[Player].handSize
        PoolSize = 52 - len(SnotConsidered)
        TotalPossibleArrangements = self.PossibleArrangements(PoolSize, PlayerHandSize)
        ArrangementsIncludingCardX = self.PossibleArrangements(PoolSize - 1, PlayerHandSize - 1)
        # TODO: Account for statements
        
        probability = ArrangementsIncludingCardX / TotalPossibleArrangements
        return probability


    # For every card, what is the prob each player is holding that card
    def gameStartCardProbabilityDistribution(self, state: MatchState, DeadCards: set):
        notConsidered = []
        notConsidered.extend([self.S(x) for x in DeadCards])
        notConsidered.extend([self.S(x) for x in state.myHand])
        print(f"Cards not considered are {notConsidered}")

        ScardsInPlay = [num for num in range(52) if num not in notConsidered]
        CardsInPlayQuantity = len(ScardsInPlay)
        dist = []

        for Scard in ScardsInPlay: 
            for playerNum in range(4):
                if playerNum != state.myPlayerNum:
                    probabilityVar = state.players[playerNum].handSize / CardsInPlayQuantity
                    dist.append([playerNum, Scard, probabilityVar])
        #print("Probability distibution: (first 10)")
        #for x in range(10):
        #    print(f"Player: {dist[x][0]}, card: {self.inverseS(dist[x][1])}, prob: {dist[x][2]} \n")
        return dist


    def adjustProbabilitiesBasedOnMatchHistory(self, state: MatchState, distribution: list, PLayersNotIncludingMe: list):
        updatedDist = []
        return updatedDist

    def tracePlayerProbability(self, state: MatchState, Player: int):
        PlayerHandSize = state.players[Player].handSize
        NoResponse = []
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
            #print(f"To beat: {toBeat}, play: {Response}")
            #StoBeat = sorted([self.S(x) for x in toBeat])
            
            if toBeat[0] == 'Start':
                print(f"Player {Player} decided to start round with {Response}")
                if len(Response) == 1:
                    if self.S(Response[0]) < self.S(lowestUnansweredSingle[0]) and state.players[Player].handSize > 3:
                        # Checks If the card would hv beaten earlier unanswered single card
                        lowestUnansweredSingle[1] = True
                        print(f"I think {Response[0]} used to belong to a higher order trick!")

            elif len(toBeat) == 5:
                if not Response:
                    trickType, determinantCard = self.TypeOfFiveCardTrick(toBeat)
                    print(f"Player {Player} did not respond to a {trickType} of order {determinantCard}!")


            elif len(toBeat) == 3:
                if not Response:
                    print(f"Player {Player} did not respond to a triple of rank {toBeat[0]}!")
   
            elif len(toBeat) == 2:
                if not Response:
                    print(f"Player {Player} did not Respond to Pair {toBeat}")

            elif len(toBeat) == 1:
                if not Response:
                    #print(f"Player {Player} did not Respond to 1 card trick: {toBeat[0]}")
                    if self.S(toBeat[0]) > self.S(lowestUnansweredSingle[0]):
                        lowestUnansweredSingle[0] = toBeat[0]
                    
                else: #if player responded, check the flag
                    if self.S(Response[0]) < self.S(lowestUnansweredSingle[0]) and state.players[Player].handSize > 3:
                         # Checks If the card would hv beaten earlier unanswered single card
                        lowestUnansweredSingle[1] = True
                        print(f"I think {Response[0]} used to belong to a higher order trick!")
        return



    def getAction(self, state: MatchState):
        action = []             # The cards you are playing for this trick
        deadCards = self.countDeadCards(state.matchHistory[-1])
        myData = state.myData   # Communications from the previous iteration
        myPlayerNum = state.myPlayerNum  # Player numbers are 0 to 3
        PlayerAfterMe = (myPlayerNum + 1) % 4
        PlayerBeforeMe = (myPlayerNum + 3) % 4
        PlayerOppositeMe = (myPlayerNum + 2) % 4
        PlayersNotIncludingMe = [PlayerAfterMe, PlayerOppositeMe, PlayerBeforeMe]

        #self.tracePlayerProbability(state, PlayerAfterMe)
        #self.tracePlayerProbability(state, PlayerOppositeMe)
        #self.tracePlayerProbability(state, PlayerBeforeMe)
        
        self.gameStartCardProbabilityDistribution(state, deadCards)
        #MyCardQuantity = self.cardsHeldByPlayer(myPlayerNum, state.players)

        ### Sort hand from lowest to highest card
        sortedHand = sorted(state.myHand, key = lambda x : self.S(x), reverse=True) 

        #for x in sortedHand:
        #    if self.Srel(x,deadCards, sortedHand) == 0:
        #        print(f"I'm holding the strongest card in the game!: {x}")


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