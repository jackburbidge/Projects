'''
A program that simulates the game of Blackjack.
'''
import random

# Create Deck of Cards
deck = []
for i in ['H', 'D', 'C', 'S']:
    for j in range(2, 11):
        deck += [i + str(j)]
    for j in ['J', 'Q', 'K', 'A']:
        deck += [i + j]

# We'll use a 6 Card Shoe
shoe = deck * 6


class Hand:
    '''
    A class for handling the dealer's and player's hands.
    '''
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
        values.sort()
        values = values[::-1]
        busted = True

        for i in values:
            if i <= 21:
                busted = False

        return busted


    def highScore(self):
        values = self.value()
        values.sort()
        value = 0

        for i in values:
            if i <= 21:
                value = i

        return value



def main():
    print('Welcome to Blackjack.')
    print('Blackjack pays 2 to 1.')
    print('Insurance pays 3 to 2.')
    print('Dealer hits until 17.')
    print('Starting Account Balance: 500')
    input('Press Enter to play.')
    print(' ')

    balance = 500           # Player's starting balance
    random.shuffle(shoe)    # Shuffle the shoe

    while balance > 0:
        # Initialize player and dealer hands
        playerHand = Hand([])
        dealerHand = Hand([])

        # Deal 2 cards to player and dealer
        for i in range(2):
            playerHand.cards += ([shoe.pop(0)])
            dealerHand.cards += ([shoe.pop(0)])

        handOver = False
        busted = False
        while not handOver:
            bet = 0
            while bet == 0:
                print('Your balance is', balance)
                bet = int(input('Please enter bet: '))

            while True:
                print('\nDealer is showing:', dealerHand.cards[0])
                print('You are showing:', playerHand.cards)
                print('''You're current score is''', playerHand.value())

                action = str()
                while action not in ['S', 'H', 'D', 'Sp']:
                    action = input('Would you like to hit (H), stand (S), or double down (D)? ').upper()
                    print(' ')

                if action == 'H':
                    playerHand.cards += ([shoe.pop(0)])

                    if playerHand.bust():
                        balance -= bet
                        handOver = True
                        busted = True
                        break

                elif action == 'D':
                    bet = bet * 2
                    playerHand.cards += ([shoe.pop(0)])

                    if playerHand.bust():
                        balance -= bet
                        handOver = True
                        busted = True

                    break

                elif action == 'S':
                    break

            if busted:
                print('You busted.')
                print('You lost this hand.\n')
                break


            print('Dealer is showing:', dealerHand.cards)
            print('You are showing:', playerHand.cards)

            dealerScore = dealerHand.highScore()
            playerScore = playerHand.highScore()
            print('''The dealer's score is''', dealerScore)
            print('''You're score is''', playerScore)

            dealerBust = False
            while dealerScore <= 16:
                dealerHand.cards += ([shoe.pop(0)])
                print('Dealer drew a', dealerHand.cards[-1])
                print('''Dealer's score is now''', dealerHand.value())

                if dealerHand.bust():
                    print('Dealer busted.')
                    print('You won this hand.\n')
                    balance += bet
                    dealerBust = True
                    break

                dealerScore = dealerHand.highScore()


            if dealerBust:
                break


            if dealerScore > playerScore:
                print('You lost this hand.')
                print('''You're bet was''', bet, '\n')
                balance -= bet
                break

            elif dealerScore < playerScore:
                print('You won this hand.')
                print('''You're bet was''', bet, '\n')
                balance += bet
                break

            else:
                print('You pushed.')
                print('''You're bet was''', bet, '\n')
                break



            print(' ')













if __name__ == '__main__':
    main()
