from random import random
from Blackjack.Card import Card

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

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