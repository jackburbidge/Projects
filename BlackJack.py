'''
A program that simulates the game of Blackjack.
'''
import random

# Create Deck of Cards
deck = []
for i in ['H', 'D', 'C', 'S']:
    for j in range(1, 11):
        deck += [i + str(j)]
    for j in ['J', 'Q', 'K', 'A']:
        deck += [i + j]

# Blackjack uses a 6 Card Shoe
shoe = deck * 6


class Hand:
    def __init__(self, cards):
        self.cards = cards
        return

    def value(self):
        # This doesn't work yet
        aces = 0
        values = []
        value = 0
        for i in self.cards:
            if i[1:] == 'A':
                aces += 1
            else:
                if i[1:] in ['J', 'Q', 'K']:
                    value += 10
                else:
                    value += int(i[1:])

        if aces == 0:
            return [value]

        for i in range(aces + 1):
            #aceCombos += [1*i + 11*(x-i)]
            if value + (1*i + 11*(aces - i)) <= 21:
                values += [value + (1*i + 11*(aces - i))]

        return values


    def bust(self):
        if self.value() > 21:
            return True
        else:
            return False
