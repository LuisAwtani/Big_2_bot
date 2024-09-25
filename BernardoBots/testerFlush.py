rank_order = {
    '3': 0, '4': 1, '5': 2, '6': 3, '7': 4,
    '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9,
    'K': 10, 'A': 11, '2': 12  # '2' is the highest rank in Big 2
}

def check_stronger_flush(flush1, flush2):
    # Sort both flushes by rank in descending order
    flush1_sorted = sorted(flush1, key=lambda card: rank_order[card[0]], reverse=True)
    flush2_sorted = sorted(flush2, key=lambda card: rank_order[card[0]], reverse=True)

    # Compare each card rank in order from highest to lowest
    for card1, card2 in zip(flush1_sorted, flush2_sorted):
        if rank_order[card1[0]] > rank_order[card2[0]] :
            return True
        elif rank_order[card1[0]] < rank_order[card2[0]]:
            return False

    # If all cards are the same in terms of rank, return False (the flushes are equal in strength)
    #TODO check edge case where both flushes have exact same ranks
    print("Fluhes are equal in strength")
    return True

Flush1 = ['4H', '8H', 'JH', 'QH', 'KH']
Flush2 = ['4S', '9S', 'JS', 'QS', 'KS']

print(check_stronger_flush(Flush1, Flush2))