from Blackjack.Deck import Deck

SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]
VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

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