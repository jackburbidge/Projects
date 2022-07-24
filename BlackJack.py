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


    def value(self):
        '''
        Returns the value of the current hands.
        '''
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
        '''
        Checks if the hand is a bust.
        '''
        values = self.value()
        values.sort()
        values = values[::-1]
        busted = True

        for i in values:
            if i <= 21:
                busted = False

        return busted


    def highScore(self):
        '''
        Determines the hand's highest value that is not a bust.
        '''
        values = self.value()
        values.sort()
        value = 0

        for i in values:
            if i <= 21:
                value = i

        return value


    def blackjack(self):
        '''
        Checks if the hand is equal to 21.
        '''
        values = self.value()
        values.sort()

        blackjack = False
        for i in values:
            if i == 21:
                return True

        return False


    @staticmethod
    def cardValue(card):
        '''
        Returns the value of a given card.
        '''
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
    print('Starting Account Balance: 100.')
    print('Minimum bet of 10.')
    input('Press Enter to play.')

    balance = 100           # Player's starting balance
    random.shuffle(shoe)    # Shuffle the shoe

    while balance > 0:
        # Initialize player and dealer hands
        playerHands = [Hand([])]
        dealerHand = Hand([])

        # Deal 2 cards to player and dealer. Player is dealt first.
        for i in range(2):
            playerHands[0].cards += ([shoe.pop(0)])
            dealerHand.cards += ([shoe.pop(0)])

        # Loop ends when the player runs out of money.
        while True:
            bet = 0
            # Basic betting boundary checks.
            while bet < 10 or type(bet) != int or bet > balance:
                print('\nYour balance is', balance)
                bet = input('Please enter bet: ')
                try:
                    bet = int(bet)
                except:
                    bet = 10

            # Subtract bet amount from player's balance
            balance -= bet

            # If dealer is showing a face card/ace check for blackjack and insurance.
            if dealerHand.cards[0][1:] in ['J', 'Q', 'K', 'A', '10']:
                print('You are showing:', playerHands[0].cards)
                print('\nDealer is showing:', dealerHand.cards[0])

                # Both the player and the dealer have blackjack.
                if playerHands[0].blackjack() and dealerHand.blackjack():
                    print('You have blackjack.')
                    print('The dealer also has blackjack.')

                    break

                # The player has blackjack and the dealer does not.
                if playerHands[0].blackjack() and not dealerHand.blackjack():
                    print('You have blackjack.')
                    balance += int(bet * 1.5)

                    break


                # Determine if the player wants insurance.
                insurance = str()
                while insurance not in ['Y', 'N']:
                    insurance = input('Would you like to buy insurance? ').upper()

                # The player opted for insurance.
                if insurance == 'Y':
                    insurance = 0
                    while insurance <= 0 or type(insurance) != int or insurance > int(bet) / 2 or insurance > balance:
                        print('Your balance is', balance)
                        print('Max insurance bet', min(int(bet / 2), balance))
                        insurance = input('Please enter insurance amount: ')
                        try:
                            insurance = int(insurance)
                        except:
                            insurance = 0

                    # If the dealer has blackjack the hand is over.
                    if dealerHand.blackjack():
                        balance += insurance
                        print('Dealer had blackjack.')
                        print('You lost this hand, but your insurance paid off.')

                        break

                    # If the dealer does not have blackjack we continue.
                    else:
                        balance -= insurance
                        print('Dealer does not have blackjack.')
                        print('Your balance is', balance)

                # The player opted out of insurance.
                if insurance == 'N':
                    # If the dealer has blackjack the hand is over.
                    if dealerHand.blackjack():
                        print('Dealer had blackjack.')
                        print('You lost this hand.')

                        break

                    # If the dealer does not have blackjack we continue.
                    else:
                        print('Dealer does not have blackjack.')

            # If the player has blackjack and the dealer is not showing a facecard
            # then the hand is over and the player is paid 1.5x their bet.
            if playerHands[0].blackjack():
                print('You have blackjack.')
                balance += int(bet * 1.5)

                break


            # Now that the checks for blackjacks are done normal play starts.
            # The hand is over once the dealer busts, the player busts, or the
            # player quits hitting.
            done = [False]
            doubled = [False]
            busted = [False]
            while True:
                # We iterate through the players hands, which may be multiple if
                # the player has split their hands.
                for i in range(len(playerHands)):
                    while not done[i]:
                        print(' ')

                        playerHand = playerHands[i]

                        # If the player has split hands, then they are forced to hit.
                        if len(playerHand.cards) == 1:
                            print('You are showing:', playerHand.cards)
                            print('The dealer draws you a card.')
                            playerHand.cards += [shoe.pop()]

                        print('Dealer is showing:', dealerHand.cards[0])
                        print('You are showing:', playerHand.cards)
                        print('''You're current score is''', playerHand.value())

                        # If the player has blackjack, they must stand.
                        if playerHand.blackjack():
                            print('You have 21. You must stand.')
                            done[i] = True

                        # Determine what the player wants to do with their hand.
                        action = str()
                        split = False
                        while action not in ['S', 'H', 'D', 'SP']:
                            # The player can split if the cards they are showing
                            # are the same. Otherwise they cannot.
                            if playerHand.cardValue(playerHand.cards[-1]) == playerHand.cardValue(playerHand.cards[-2]) and balance >= bet:
                                action = input('Would you like to hit (H), stand (S), double down (D), or split (SP)? ').upper()
                                split = True
                            else:
                                action = input('Would you like to hit (H), stand (S), or double down (D)? ').upper()

                        # If the player chose to split, they are now playing
                        # two hands.
                        if action == 'SP' and split:
                            balance -= bet
                            playerHands += [Hand([playerHand.cards.pop()])]
                            done += [False]
                            doubled += [False]
                            busted += [False]

                        # If the player chose to hit, they are given another card.
                        elif action == 'H':
                            playerHand.cards += ([shoe.pop(0)])
                            print('You drew a', playerHand.cards[-1])
                            print('''You're score is''', playerHand.value())

                            # If the player busted, this hand is over.
                            if playerHand.bust():
                                print('You busted.')
                                busted[i] = True
                                done[i] = True

                            # If the player has 21, they must stand.
                            if playerHand.blackjack():
                                print('You have 21. You must stand.')
                                done[i] = True

                        # If the player doubles down they get another card and
                        # they are not allowed to hit again.
                        elif action == 'D':
                            balance -= min(bet, balance)
                            playerHand.cards += ([shoe.pop(0)])
                            print('You drew a', playerHand.cards[-1])
                            print('''You're score is''', playerHand.value())

                            if playerHand.bust():
                                print('You busted.')
                                busted[i] = True

                            done[i] = True
                            doubled[i] = True

                        # If the player decides to stand, we stop player action.
                        elif action == 'S':
                            done[i] = True

                # If all hands are done taking action, we can exit this loop
                # and move on to determining winners of the hand.
                if sum(done) == len(done):
                    break

            # If all of the players hands have busted, the round is over.
            if sum(busted) == len(busted):
                break

            print('Dealer is showing:', dealerHand.cards)
            print('You are showing:', playerHand.cards)

            dealerScore = dealerHand.highScore()
            print('''The dealer's score is''', dealerScore)


            # If dealer's score is less than 17, draw from the deck.
            dealerBust = False
            while dealerScore < 17:
                dealerHand.cards += ([shoe.pop(0)])
                print('Dealer drew ', dealerHand.cards[-1])
                print('''Dealer's score is now''', dealerHand.value())

                # If the dealer busts, the player wins all of its hands.
                if dealerHand.bust():
                    print('Dealer busted.')
                    print('You won this hand.')

                    # Iterate through the players hands to add bets to their
                    # cash balance.
                    for i in range(len(playerHands)):
                        if not busted[i]:
                            balance += 2 * bet * (1 + doubled[i])
                    dealerBust = True

                    break

                dealerScore = dealerHand.highScore()

            # If dealer busted, the round is over.
            if dealerBust:
                break


            # Calculate who wins the hand, since we know the dealer didn't bust.
            for i in range(len(playerHands)):
                if not busted[i]:
                    playerHand = playerHands[i]
                    playerScore = playerHand.highScore()
                    print('\nYou are showing:', playerHand.cards)

                    # The player's hand lost to the dealer's.
                    if dealerScore > playerScore:
                        print('''You're score is''', playerScore)
                        print('You lost this hand.')
                        print('''You're bet was''', bet * (1 + doubled[i]))

                    # The player's hand beat the dealer's
                    elif dealerScore < playerScore:
                        print('''You're score is''', playerScore)
                        print('You won this hand.')
                        print('''You're bet was''', bet * (1 + doubled[i]))
                        balance += 2 * bet * (1 + doubled[i])

                    # If the player and dealer tie, the player gets its bet back.
                    else:
                        print('''You're score is''', playerScore)
                        print('You pushed.')
                        print('''You're bet was''', bet * (1 + doubled[i]))
                        balance += bet * (1 + doubled[i])

            break

    print('\n\n\nYou lost the game.')




if __name__ == '__main__':
    main()
