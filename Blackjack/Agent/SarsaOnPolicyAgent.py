from Blackjack.Agent.Agent import Agent
from Blackjack.Action import Action

from random import random, choice
from math import exp

class SarsaOnPolicyAgent(Agent):
    def __init__(self, epsilon_type):
        super().__init__()

        self.episode_count = 1
        self.current_episode = []
        self.epsilon_type = epsilon_type
        self.epsilon = self.compute_epsilon()

    def compute_epsilon(self):
        if self.epsilon_type == 1:
            return 0.1
        elif self.epsilon_type == 2:
            return 1 / self.episode_count
        elif self.epsilon_type == 3:
            return exp(-self.episode_count / 1000)
        elif self.epsilon_type == 4:
            return exp(-self.episode_count / 10000)
        else: 
            raise ValueError("Invalid epsilon")
        
    def get_policy(self, state):
        # hit below 12, stand above 21 always
        # no need to update n counter or q values since these are trivial states
        if state ["agent_sum"] < 12:
            return Action.HIT
        elif state ["agent_sum"] >= 21:
            return Action.STAND

        possible_actions = [action for action in Action]

        if random() < self.epsilon: # selected randomly
            chosen_action = choice(possible_actions)  
        else: # selected greedily
            q_values_by_action = {action: self.get_q_value(state, action) for action in possible_actions}

            chosen_action = max(q_values_by_action, key = q_values_by_action.get)

        self.increment_n_counter(state, chosen_action)
        self.current_episode.append((state, chosen_action))

        return chosen_action
    
    def update_agent(self, next_state, next_action, reward):
        if not self.current_episode:
            return

        reward = 0 if reward is None else reward # non-terminal states are assumed to have a reward of 0

        prev_state, prev_action = self.current_episode [-1]
        alpha = 1 / (self.get_n_count(prev_state, prev_action) + 1)

        prev_q_value = self.get_q_value(prev_state, prev_action)
        next_q_value = self.get_q_value(next_state.get_agent_state(), next_action)
        
        new_expected_value = prev_q_value + alpha * (reward + next_q_value - prev_q_value) # equation given gamma = 1

        self.update_q_value(prev_state, prev_action, new_expected_value)

    def end_episode(self):
        self.episode_count += 1
        self.current_episode = []
        self.epsilon = self.compute_epsilon()