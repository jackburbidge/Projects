'''
A program that simulates the game of Black Jack.
'''
import random

# Create Deck of Cards
deck = []
for i in ['H', 'D', 'C', 'S']:
    for j in range(1, 11):
        deck += [i + str(j)]
    for j in ['J', 'Q', 'K', 'A']:
        deck += [i + j]

# Black Jack uses a 6 Card Shoe
shoe = deck * 6


class Hand:
    def __init__(self, cards):
        self.cards = cards
        return

    def value(self):
        # This doesn't work yet
        aces = []
        value = 0
        for i in self.cards:
            if i[1] == 'A':
                aces += [True]
            else:
                aces += [False]
                if type(i) == str:
                    value += 10
                else:
                    value += i[1]
        aces = sum(aces)

        if aces == 0:
            return value

        for i in range(aces + 1):
            #aceCombos += [1*i + 11*(x-i)]
            if value + (1*i + 11*(aces - i)) <= 21:
                newValue = value + (1*i + 11*(aces - i))

        return newValue


    def bust(self):
        if self.value() > 21:
            return True
        else:
            return False
