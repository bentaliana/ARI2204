from Blackjack.Agent.Agent import Agent
from Blackjack.Action import Action

from random import choice

class BaselineAgent(Agent):
    def get_policy(self, state):
        if state ["agent_sum"] < 12:
            return Action.HIT
        elif state ["agent_sum"] >= 21:
            return Action.STAND
        
        possible_actions = [action for action in Action]

        return choice(possible_actions)