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
        aces = 0
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

        values = []
        for i in range(aces + 1):
            values += [value + (1*i + 11*(aces - i))]

        return values



    def bust(self):
        values = self.value()
        busted = False

        for i in values:
            if i > 21:
                busted = True

        return busted



def main():
    input('Welcome to Blackjack. Press Enter to play.')
    print(' ')

    balance = 100           # Start with $100 balance
    random.shuffle(shoe)    # Shuffle the shoe

    while balance > 0:
        playerHand = Hand([])
        dealerHand = Hand([])
        for i in range(2):
            playerHand.cards += ([shoe.pop(0)])
            dealerHand.cards += ([shoe.pop(0)])


        print('Dealer cards:', dealerHand.cards[0])
        print('''You're cards:''', playerHand.cards)

        input('Would you like to hit (H), stand (S), or double down (D)? ')



if __name__ == '__main__':
    main()
