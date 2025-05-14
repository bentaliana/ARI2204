from Blackjack.Action import Action

class Dealer():
    def get_policy(self, sum):
        # Assuming dealer stands at 21
        if sum < 17 and sum <= 21:
            return Action.HIT
        else:
            return Action.STAND