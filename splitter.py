import random

# function to generate a random hand of 13 cards
def generateHand():
    hand = []
    ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
    suits = ['D', 'C', 'H', 'S']
    for i in range(13):
        randomCard = ranks[random.randint(0, 12)] + suits[random.randint(0, 3)]
        while randomCard in hand:
            randomCard = ranks[random.randint(0, 12)] + suits[random.randint(0, 3)]
        hand.append(randomCard)
    return hand


# section to sort a hand
rankOrder = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
suitOrder = {'D': 0, 'C': 1, 'H': 2, 'S': 3}

def cardValueByRank(card):
    rank = card[0]
    suit = card[1]
    return (rankOrder[rank], suitOrder[suit])

def cardValueBySuit(card):
    rank = card[0]
    suit = card[1]
    return (suitOrder[suit], rankOrder[rank])


# function to find singles in a hand
def findSingles(hand):
    singles = hand
    return singles


## NOTE: Does this function assume hand is sorted by S? If not, it might be a good idea to sort
# function to find pairs in a hand
def findPairs(hand):
    pairs = []
    for i in range(0, len(hand)):
        for j in range(i + 1, len(hand)):
            if hand[i][0] == hand[j][0]:
                pairs.append([hand[i], hand[j]])
            else:
                break
    return pairs


# function to find triples in a hand
def findTriples(hand):
    triples = []
    for i in range(0, len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                if hand[i][0] == hand[j][0] == hand[k][0]:
                    triples.append([hand[i], hand[j], hand[k]])
                else:
                    break
    return triples

# NOTE: for high order tricks, put strongest card at the front of the list/tuple
# function to find straights in a hand
def findStraights(hand):
    straights = []
    for i in range(0, len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                for l in range(k + 1, len(hand)):
                    for m in range(l + 1, len(hand)):
                        if rankOrder[hand[i][0]] + 4 == rankOrder[hand[j][0]] + 3 == rankOrder[hand[k][0]] + 2 == rankOrder[hand[l][0]] + 1 == rankOrder[hand[m][0]]:
                            if hand[i][1] == hand[j][1] == hand[k][1] == hand[l][1] == hand[m][1]:
                                continue
                            else:
                                straights.append([hand[i], hand[j], hand[k], hand[l], hand[m]])
    return straights


# function to find flushes in a hand
def findFlushes(hand):
    flushes = []
    for i in range(0, len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                for l in range(k + 1, len(hand)):
                    for m in range(l + 1, len(hand)):
                        if hand[i][1] == hand[j][1] == hand[k][1] == hand[l][1] == hand[m][1]:
                            if rankOrder[hand[i][0]] + 4 == rankOrder[hand[j][0]] + 3 == rankOrder[hand[k][0]] + 2 == rankOrder[hand[l][0]] + 1 == rankOrder[hand[m][0]]:
                                continue
                            else:
                                flushes.append([hand[i], hand[j], hand[k], hand[l], hand[m]])
    return flushes


# function to find full houses in a hand
def findFullHouses(pairs, triples):
    fullHouses = []
    for pair in pairs:
        for triple in triples:
            fail = False
            for card in triple:
                if card in pair:
                    fail = True
                    break
            if not fail:
                fullHouses.append(pair + triple)
    return fullHouses


# function to find four of a kinds in a hand
def findFourOfAKinds(hand):
    fourOfAKinds = []
    for i in range(0, len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                for l in range(k + 1, len(hand)):
                    if hand[i][0] == hand[j][0] == hand[k][0] == hand[l][0]:
                        for m in range(0, len(hand)):
                            if m != i and m != j and m != k and m != l:
                                fourOfAKinds.append([hand[i], hand[j], hand[k], hand[l], hand[m]])
    return fourOfAKinds


# function to find straight flushes in a hand
def findStraightFlushes(hand):
    straightFlushes = []
    for i in range(0, len(hand)):
        for j in range(i + 1, len(hand)):
            for k in range(j + 1, len(hand)):
                for l in range(k + 1, len(hand)):
                    for m in range(l + 1, len(hand)):
                        if rankOrder[hand[i][0]] + 4 == rankOrder[hand[j][0]] + 3 == rankOrder[hand[k][0]] + 2 == rankOrder[hand[l][0]] + 1 == rankOrder[hand[m][0]]:
                            if hand[i][1] == hand[j][1] == hand[k][1] == hand[l][1] == hand[m][1]:
                                straightFlushes.append([hand[i], hand[j], hand[k], hand[l], hand[m]])
    return straightFlushes


# def findAllSplitsFromCombinedCombinations(hand, allCombinations):
#     # Base case: if hand is empty, return a valid split (no more cards to split)
#     if not hand:
#         return [[]]

#     splits = []

#     # Try each combination (singles, pairs, triples, five-card hands)
#     for combination in allCombinations:
#         if isSubset(combination, hand):
#             remainingHand = removeCards(hand, combination)
#             for split in findAllSplitsFromCombinedCombinations(remainingHand, allCombinations):
#                 splits.append([combination] + split)

#     return splits

# def removeCards(hand, cards):
#     """
#     Given a hand and a list of cards, return a new hand with those cards removed.
#     """
#     handCopy = hand[:]
#     for card in cards:
#         handCopy.remove(card)
#     return handCopy

# def isSubset(subset, hand):
#     """
#     Check if all cards in 'subset' are available in 'hand'.
#     """
#     handCopy = hand[:]
#     for card in subset:
#         if card not in handCopy:
#             return False
#         handCopy.remove(card)
#     return True


# def removeCards(hand, cards):
#     """
#     Given a hand and a list of cards, return a new hand with those cards removed.
#     """
#     handCopy = hand[:]
#     for card in cards:
#         handCopy.remove(card)
#     return handCopy

# def isSubset(subset, hand):
#     """
#     Check if all cards in 'subset' are available in 'hand'.
#     """
#     handCopy = hand[:]
#     for card in subset:
#         if card not in handCopy:
#             return False
#         handCopy.remove(card)
#     return True


# main function
def main():
    print("Press enter to generate a hand:")
    enter = input()
    hand = generateHand()
    print(hand, "\n")

    print("Press enter to sort the hand by rank:")
    enter = input()
    sortedHandByRank = sorted(hand, key=cardValueByRank)
    print(sortedHandByRank, "\n")

    print("Press enter to sort the hand by suit:")
    enter = input()
    sortedHandBySuit = sorted(hand, key=cardValueBySuit)
    print(sortedHandBySuit, "\n")

    hand = sortedHandByRank

    print("Press enter to find singles:")
    enter = input()
    singles = findSingles(hand)
    print(singles, "\n")

    print("Press enter to find pairs:")
    enter = input()
    pairs = findPairs(hand)
    print(pairs, "\n")

    print("Press enter to find triples:")
    enter = input()
    triples = findTriples(hand)
    print(triples, "\n")

    print("Press enter to find straights:")
    enter = input()
    straights = findStraights(hand)
    print(straights, "\n")

    print("Press enter to find flushes:")
    enter = input()
    flushes = findFlushes(hand)
    print(flushes, "\n")

    print("Press enter to find full houses:")
    enter = input()
    fullHouses = findFullHouses(pairs, triples)
    print(fullHouses, "\n")

    print("Press enter to find four of a kinds:")
    enter = input()
    fourOfAKinds = findFourOfAKinds(hand)
    print(fourOfAKinds, "\n")

    print("Press enter to find straight flushes:")
    enter = input()
    straightFlushes = findStraightFlushes(hand)
    print(straightFlushes, "\n")

    # print("Press enter to find all possible splits:")
    # enter = input()
    # allSplits = []
    # for split in allSplits:
    #     print(split)


if __name__ == "__main__":
    main()