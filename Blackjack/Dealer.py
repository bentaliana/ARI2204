from Blackjack.Action import Action

class Dealer():
    def get_policy(self, sum):
        if sum < 17:
            return Action.HIT
        else:
            return Action.STAND