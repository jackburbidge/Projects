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


    def blackjack(self):
        values = self.value()
        values.sort()

        blackjack = False
        for i in values:
            if i == 21:
                return True

        return False


    @staticmethod
    def cardValue(card):
        if card[1:] in ['J', 'Q', 'K']:
            return 10

        elif card[1:] == 'A':
            return [1, 11]

        else:
            return int(card[1:])



def main():
    print('Welcome to Blackjack.')
    print('Blackjack pays 3 to 2.')
    print('Insurance pays 2 to 1.')
    print('Dealer hits until 17.')
    print('Starting Account Balance: 500')
    input('Press Enter to play.')

    balance = 500           # Player's starting balance
    random.shuffle(shoe)    # Shuffle the shoe

    while balance > 0:
        # Initialize player and dealer hands
        playerHands = [Hand([])]
        dealerHand = Hand([])

        # Deal 2 cards to player and dealer
        for i in range(2):
            #playerHands[0].cards += ([shoe.pop(0)])
            dealerHand.cards += ([shoe.pop(0)])
        playerHands[0].cards = ['S10', 'HK']

        while True:
            bet = 0
            while bet <= 0 or type(bet) != int:
                print('\nYour balance is', balance)
                bet = input('Please enter bet: ')
                try:
                    bet = int(bet)
                except:
                    bet = 0

            if dealerHand.cards[0][1:] in ['J', 'Q', 'K', 'A', '10']:
                print('\nDealer is showing:', dealerHand.cards[0])

                insurance = str()
                while insurance not in ['Y', 'N']:
                    insurance = input('Would you like to buy insurance? ').upper()

                if insurance == 'Y':
                    insurance = 0
                    while insurance <= 0 or type(insurance) != int:
                        print('Your balance is', balance)
                        print('Max insurance bet', int(bet / 2))
                        insurance = input('Please enter insurance amount: ')
                        try:
                            insurance = int(bet)
                        except:
                            insurance = 0

                    if dealerHand.blackjack():
                        balance += insurance
                        print('Dealer had blackjack.')
                        print('You lost this hand.')
                        break

                    else:
                        balance -= insurance
                        print('Dealer does not have blackjack.')
                        print('Your balance is', balance)

                if insurance == 'N':
                    pass


            while True:
                done = [False]
                doubled = [False]
                for i in range(len(playerHands)):
                    playerHand = playerHands[i]
                    print('\nDealer is showing:', dealerHand.cards[0])
                    print('You are showing:', playerHand.cards)

                    if len(playerHand.cards) == 1:
                        print('The dealer draws you a card.')
                        playerHand.cards += [shoe.pop()]

                    print('''You're current score is''', playerHand.value())


                    action = str()
                    while action not in ['S', 'H', 'D', 'SP']:
                        if playerHand.cardValue(playerHand.cards[-1]) == playerHand.cardValue(playerHand.cards[-2]):
                            action = input('Would you like to hit (H), stand (S), double down (D), or split (SP)? ').upper()
                        else:
                            action = input('Would you like to hit (H), stand (S), or double down (D)? ').upper()
                        #print(' ')

                    if action == 'SP':
                        playerHands += [Hand([playerHand.cards.pop()])]
                        done += [False]
                        doubled += [False]

                    elif action == 'H':
                        playerHand.cards += ([shoe.pop(0)])
                        print('You drew a', playerHand.cards[-1])
                        print('''You're score is''', playerHand.value())

                        if playerHand.bust():
                            balance -= bet
                            #done[i] = True
                            #doubled[i] = False
                            playerHands.pop(i)
                            done.pop(i)
                            doubled.pop(i)
                            print('You busted.')
                            balance -= bet
                            break

                    elif action == 'D':
                        playerHand.cards += ([shoe.pop(0)])

                        if playerHand.bust():
                            balance -= bet
                            #done[i] = True
                            #doubled[i] = False
                            playerHands.pop(i)
                            done.pop(i)
                            doubled.pop(i)
                            print('You busted.')
                            balance -= bet
                            break

                        done[i] = True
                        doubled[i] = True

                        break

                    elif action == 'S':
                        done[i] = True
                        doubled[i] = False
                        break

                if sum(done) == len(done):
                    break

            if len(playerHands) == 0:
                break

            print('Dealer is showing:', dealerHand.cards)
            print('You are showing:', playerHand.cards)

            dealerScore = dealerHand.highScore()
            print('''The dealer's score is''', dealerScore)


            # If dealer's score is less than 17, draw from the deck
            dealerBust = False
            while dealerScore < 17:
                dealerHand.cards += ([shoe.pop(0)])
                print('Dealer drew a', dealerHand.cards[-1])
                print('''Dealer's score is now''', dealerHand.value())

                if dealerHand.bust():
                    print('Dealer busted.')
                    print('You won this hand.')
                    for i in range(len(playerHands)):
                        balance += bet * (1 + doubled[i])
                    dealerBust = True
                    break

                dealerScore = dealerHand.highScore()

            # If dealer busted, we exit the loop
            if dealerBust:
                break


            # Calculate who wins the hand
            for i in range(len(playerHands)):
                playerScore = playerHands[i].highScore()
                if dealerScore > playerScore:
                    print('''You're score is''', playerScore)
                    print('You lost this hand.')
                    print('''You're bet was''', bet * (1 + doubled[i]))
                    balance -= bet * (1 + doubled[i])
                    break

                elif dealerScore < playerScore:
                    print('''You're score is''', playerScore)
                    print('You won this hand.')
                    print('''You're bet was''', bet * (1 + doubled[i]))
                    balance += bet * (1 + doubled[i])
                    break

                else:
                    print('''You're score is''', playerScore)
                    print('You pushed.')
                    print('''You're bet was''', bet * (1 + doubled[i]))
                    break

            break
















if __name__ == '__main__':
    main()
