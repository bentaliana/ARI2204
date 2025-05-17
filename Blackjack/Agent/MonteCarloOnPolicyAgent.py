from Blackjack.Agent.Agent import Agent
from Blackjack.Action import Action

from random import choice, random
from math import exp

class MonteCarloOnPolicyAgent(Agent):
    def __init__(self, exploring_starts, epsilon_type):
        super().__init__()

        self.exploring_starts = exploring_starts
        self.first_state = True
        self.episode_count = 1
        self.current_episode = []
        self.epsilon = 0
        self.epsilon_type = epsilon_type
        
        # consider k = 1 (the episode count is 1)
        if self.epsilon_type == 1: # epsilon is 1 / k
            self.epsilon = 1
        elif self.epsilon_type == 2: # epsilon is e ^ (-k / 1000) 
            self.epsilon = exp(-1 / 1000)
        elif self.epsilon_type == 3: # epsilon is e ^ (-k / 10000)
            self.epsilon = exp(-1 / 10000)
        else:
            raise ValueError("Epsilon type not understood")

    def get_policy(self, state):
        # hit below 12, stand above 21
        # no need to update n counter or q values since these are trivial states
        if state ["agent_sum"] < 12:
            return Action.HIT
        elif state ["agent_sum"] >= 21:
            return Action.STAND

        possible_actions = [action for action in Action]

        if self.exploring_starts and self.first_state: # exploring starts for the first state
            self.first_state = False

            chosen_action = choice(possible_actions)
        elif random() < self.epsilon: # selected randomly
            chosen_action = choice(possible_actions)  
        else: # selected greedily
            q_values_by_action = {action: self.get_q_value(state, action) for action in possible_actions}

            chosen_action = max(q_values_by_action, key = q_values_by_action.get)

        self.increment_n_counter(state, chosen_action)
        self.current_episode.append((state, chosen_action))

        return chosen_action
    
    def update_agent(self, state):
        # updating the q values, given that the discount factor is 1
        reward = state.get_terminal_state(True)

        for state, action in self.current_episode:
            current_expected_value = self.get_q_value(state, action)
            new_expected_value = current_expected_value + (1 / self.get_n_count(state, action)) * (reward - current_expected_value)

            self.update_q_value(state, action, new_expected_value)

    def end_episode(self):
        self.episode_count += 1
        self.current_episode = []
        self.first_state = True

        # updating the epsilon value
        if self.epsilon_type == 1: # epsilon is 1 / k
            self.epsilon = 1 / self.episode_count
        elif self.epsilon_type == 2: # epsilon is e ^ (-k / 1000) 
            self.epsilon = exp(-self.episode_count / 1000)
        elif self.epsilon_type == 3: # epsilon is e ^ (-k / 10000)
            self.epsilon = exp(-self.episode_count / 10000)