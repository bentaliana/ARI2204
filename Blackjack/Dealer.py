class Dealer():
    def get_policy(self, sum):
        # Assume dealer stands at 21
        # TODO: should we change it to hit at 21? its a bit ambiguous in the project brief
        if sum < 17 and sum <= 21:
            return True # Hit
        else:
            return False # Stand