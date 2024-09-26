COMBO_ORDER = {'straight': 0, 'flush': 1, 'full house': 2, 'four-of-a-kind': 3, 'straight flush': 4}
RANK_ORDER = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
SUIT_ORDER = {'?': 0, 'D': 1, 'C': 2, 'H': 3, 'S': 4}

def sortCards(cards): # returns a list of cards sorted by rank and suit
    return sorted(cards, key=lambda card: (RANK_ORDER.get(card[0], 99), SUIT_ORDER.get(card[1], 99)))

def S(card: str):
    ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
    suits = ['S', 'H', 'C', 'D']
    rating = ranks.index(card[0]) * 4 + suits.index(card[1])
    return rating

def inverseS(rating: int):
    ranks = ['2', 'A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3']
    suits = ['S', 'H', 'C', 'D']
    index = rating // 4
    suitIndex = rating % 4
    return ranks[index] + suits[suitIndex]

def compareFlushes(flush1, flush2):
    flush1 = sortCards(flush1)
    flush2 = sortCards(flush2)
    #print("Comparing flushes...")
    #print("Flush 1: ", flush1)
    #print("Flush 2: ", flush2)
    for i in range(4, -1, -1):
        if RANK_ORDER[flush1[i][0]] > RANK_ORDER[flush2[i][0]]:
            print("Flush 1 wins")
            return True
        elif RANK_ORDER[flush1[i][0]] < RANK_ORDER[flush2[i][0]]:
            print("Flush 2 wins")
            return False
    if SUIT_ORDER[flush1[0][1]] > SUIT_ORDER[flush2[0][1]]:
        print("Flush 1 wins")
        return True
    else:
        print("Flush 2 wins")
        return False

def typeOfFiveCardTrick(trick: list):
    Strick = sorted([S(x) for x in trick])
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
        return "straight flush", inverseS(strongest)
    
    cardRanks = [inverseS(x)[0] for x in Strick]
    if len(set(cardRanks)) == 2: # If only 2 ranks exist in the set, Its Fours' of Full House
        if 4 > cardRanks.count(cardRanks[0]) > 1:  # if its a Full House
            if cardRanks[2] != cardRanks[0]:   # Find determining (triplet) rank if its full house
                return "full house", inverseS(Strick[4])
            else:
                return "full house", inverseS(strongest)
        else:  # Else we have Four of a kind
            if inverseS(Strick[1])[0] == inverseS(Strick[0])[0]:
                return "four-of-a-kind", inverseS(Strick[0])
            else:
                return "four-of-a-kind", inverseS(Strick[1])

    cardSuits = [inverseS(x)[1] for x in Strick]
    if len(set(cardSuits)) == 1:
        return "flush", inverseS(strongest)
    else:
        return "straight", inverseS(strongest)

def isStrongerTrick(trick1Type, trick1Strongest, trick2Type, trick2Strongest, trick1, trick2):
    # First, compare the trick types
    if COMBO_ORDER[trick1Type] > COMBO_ORDER[trick2Type]:
        return True
    elif COMBO_ORDER[trick1Type] < COMBO_ORDER[trick2Type]:
        return False
    if trick1Type == 'flush':
        return compareFlushes(trick1, trick2)
    # Compare card values first
    if S(trick1Strongest) < S(trick2Strongest):
        return True
    else:
        return False

def isStrongerPair(pair1, pair2):
    determinant1 = pair1[0]
    if S(pair1[1]) < S(pair1[0]):
        determinant1 = pair1[1]
    determinant2 = pair2[0]
    if S(pair2[1]) < S(pair2[0]):
        determinant2 = pair2[1]
    if S(determinant1) < S(determinant2):
        return True
    else:
        return False
      
def isStrongerTriple(triple1, triple2):
    determinant1 = triple1[0]
    determinant2 = triple2[0]
    if S(determinant1) < S(determinant2):
        return True
    else:
        return False

def canBeat(trick: list[str], currentTrick: list[str]):
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
            if S(trick[0]) < S(currentTrick[0]):
                return True
            else:
                return False
        #if they're both pairs
        elif championLen == 2:
            if isStrongerPair(trick, currentTrick):
                return True
            else:
                return False
        #if they're both triples
        elif championLen == 3:
            if isStrongerTriple(trick, currentTrick):
                return True
            else:
                return False
        elif championLen == 5:
            # Determinant refers to the strongest (determining) card in that trick
            challengerTrickType, challengerDeterminant = typeOfFiveCardTrick(trick)
            championTrickType, championDeterminant = typeOfFiveCardTrick(currentTrick)
            if isStrongerTrick(challengerTrickType, challengerDeterminant, championTrickType, championDeterminant, trick, currentTrick):
                return True
        # No else branch, please notify me if we get return NoneType bug
            else:
                return False

# First, pass the current trick on the table as a list of cards.
# Then, pass the list of non-control tricks and control tricks, where each trick is a list of cards of length 1, 2, 3, or 5.
# The function returns a boolean indicating whether a winning sequence was found, and the winning sequence if it exists.
def checkForWinningSequence(currentTrick, nonControlTricks: list[list[str]], controlTricks: list[list[str]]):
    if len(controlTricks) >= len(nonControlTricks) - 1:
        # try to match up one control trick with one non control trick of the same trick length
            matches = []
            controlTrickUsed = []
            for nonControlTrick in nonControlTricks:
                for i in range(len(controlTricks)):
                    if i not in controlTrickUsed:
                        if len(controlTricks[i]) == len(nonControlTrick):
                            matches.append([nonControlTrick, controlTricks[i]])
                            controlTrickUsed.append(i)
                            break
            if len(matches) >= len(nonControlTricks) - 1:
                winningSequence = []
                found = False
                if len(nonControlTricks) == len(controlTricks) + 1: # NCNCNCN
                    for i in range(len(matches)):
                        nonControlTrick = matches[i][0]
                        if currentTrick is None or canBeat(nonControlTrick, currentTrick):
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
                        if currentTrick is None or canBeat(controlTrick, currentTrick):
                            matches[i], matches[0] = matches[0], matches[i]
                            found = True
                            break
                    if found:
                        winningSequence.append(matches[0][1])
                        for i in range(1, len(matches)):
                            winningSequence.append(matches[i][0])
                            winningSequence.append(matches[i][1])
                        winningSequence.append(matches[0][0])
                        return True, winningSequence
                    for i in range(len(matches)):
                        nonControlTrick = matches[i][0]
                        if currentTrick is None or canBeat(nonControlTrick, currentTrick):
                            matches[i], matches[0] = matches[0], matches[i]
                            found = True
                            break
                    if found:
                        for match in matches:
                            winningSequence.append(match[0])
                            winningSequence.append(match[1])
                        winningSequence[-2], winningSequence[-1] = winningSequence[-1], winningSequence[-2]
                        return True, winningSequence

                else: # CCCCNCNC or NCCCCCNC
                    for controlTrick in controlTricks:
                        if controlTrick not in controlTrickUsed:
                            if currentTrick is None or canBeat(controlTrick, currentTrick):
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
                        return True, winningSequence
                    for i in range(len(matches)):
                        nonControlTrick = matches[i][0]
                        if currentTrick is None or canBeat(nonControlTrick, currentTrick):
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
                        return True, winningSequence
    return False, []

