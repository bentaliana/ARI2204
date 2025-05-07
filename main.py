from Blackjack.Round import Round
from Blackjack.Dealer import Dealer

class Game():
    def play_round(self):
        self.round = Round()

        action = "h"

        while action == "h" and self.round.get_terminal_state() == None and self.round.get_sum_for_player(True) != 21:
            self.round.print_terminal_state()

            print(self.round.get_agent_state())

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

        if self.round.get_terminal_state() != None:
            print("\n\nRound over!")
            self.round.print_terminal_state()
            return
        
        # Automatically stand for player if they have 21 from the start, or if they reach 21 after hitting
        if self.round.get_sum_for_player(True) == 21:
            self.round.print_terminal_state()
            self.round.stand() # Change turn to dealer

        dealer = Dealer()

        while dealer.get_policy(self.round.get_sum_for_player(False)) == True and self.round.get_terminal_state() == None:
            print("\nDealer hits")
            self.round.hit()

            self.round.print_terminal_state()

        print("\n\nRound over!")
        self.round.print_terminal_state(True)

game = Game()

game.play_round()