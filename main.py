from random import random

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class Deck():
    def __init__(self):
        self.cards = []

        for suit in SUITS:
           for value in VALUES:
               self.cards.append(Card(suit, value))

    def shuffle(self):
        # Assuming that we can't use a built-in function for shuffling:
        # Give each card a random number between 0 and 1 and sort the deck on that random number
        cards_shuffle_value = []

        for card in self.cards:
            cards_shuffle_value.append((card, random()))
        
        cards_shuffle_value.sort(key = lambda card_shuffle_value: card_shuffle_value [1])

        self.cards = [card_shuffle_value [0] for card_shuffle_value in cards_shuffle_value]

    def get_next_card(self):
        return self.cards.pop()

class Round():
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        
        self.player_cards = [self.deck.get_next_card(), self.deck.get_next_card()] # 2 cards for player
        self.dealer_cards = [self.deck.get_next_card()] # 1 card for dealer

        self.player_turn = True # Player always starts

    def hit(self):
        if self.player_turn == True:
            self.player_cards.append(self.deck.get_next_card())
        else:
            self.dealer_cards.append(self.deck.get_next_card())

    def stand(self):
        self.player_turn = not(self.player_turn)

    def get_sum_for_player(self, player_turn):
        cards = []

        if player_turn == True:
            cards = self.player_cards
        else:
            cards = self.dealer_cards

        contains_ace = False
        sum = 0

        for card in cards:
            if card.value == "A":
                contains_ace = True
            
            if card.value in ["J", "Q", "K"]:
                sum += 10
            else:
                sum += VALUES.index(card.value) + 1

        # Allow ace to count as 11 rather than 1
        if contains_ace and sum <= 11:
            sum += 10

        return sum
    
    def print_state(self, force_end = False):
        player_sum = self.get_sum_for_player(True)
        dealer_sum = self.get_sum_for_player(False)

        print(f"\nCards for player: {[card.value for card in self.player_cards]}")
        print(f"Sum for player: {player_sum}")

        print(f"\nCards for dealer: {[card.value for card in self.dealer_cards]}")
        print(f"Sum for dealer: {dealer_sum}")

        round_state = self.get_state(force_end)

        if round_state == 1:
            print("Player won")
        elif round_state == -1:
            print("Player lost")
        elif round_state == 0:
            print("Draw")

    def get_state(self, force_end = False):
        player_sum = self.get_sum_for_player(True)
        dealer_sum = self.get_sum_for_player(False)
        
        if dealer_sum > 21:
            return 1 # Win
        elif player_sum > 21:
            return -1 # Loss
        elif player_sum == 21 and dealer_sum == 21:
            return 0 # Draw
        
        if force_end == True:
            if player_sum > dealer_sum:
                return 1
            elif player_sum < dealer_sum:
                return -1
            else:
                return 0
        else:
            return None # Game still in progress

class Dealer():
    def get_policy(self, sum):
        # Assume dealer stands at 21
        # TODO: should we change it to hit at 21? its a bit ambiguous in the project brief
        if sum < 17 and sum <= 21:
            return True # Hit
        else:
            return False # Stand


class Game():
    def play_round(self):
        self.round = Round()

        action = "h"

        # Automatically stand for player if they have 21 from the start
        if self.round.get_sum_for_player(True) == 21:
            self.round.print_state(True)
            self.round.stand()

        while action == "h" and self.round.get_state() == None and self.round.get_sum_for_player(True) != 21:
            self.round.print_state()

            action = input("\nDo you want to hit (h) or stand (s)?: ")

            if action == "h":
                self.round.hit()
                print("Hitting...")
            elif action == "s":
                self.round.stand()
                print("Standing...")
            else:
                print("Invalid input")
                action = "h"

        if self.round.get_state() != None:
            print("\n\nRound over!")
            self.round.print_state()
            return

        dealer = Dealer()

        while dealer.get_policy(self.round.get_sum_for_player(False)) == True and self.round.get_state() == None:
            print("\nDealer hits")
            self.round.hit()

            self.round.print_state()

        print("\n\nRound over!")
        self.round.print_state(True)

game = Game()

game.play_round()