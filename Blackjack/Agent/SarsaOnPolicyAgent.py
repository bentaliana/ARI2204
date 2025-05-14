from Blackjack.Agent.Agent import Agent
from Blackjack.Action import Action

from random import random, choice
from math import exp

class SarsaOnPolicyAgent(Agent):
    def __init__(self, epsilon_type):
        super().__init__()

        self.episode_count = 1
        self.current_episode = []
        self.epsilon = 0
        self.epsilon_type = epsilon_type

        # consider k = 1 (the episode count is 1)
        if self.epsilon_type == 1:
            self.epsilon = 0.1
        elif self.epsilon_type == 2: # epsilon is 1 / k
            self.epsilon = 1
        elif self.epsilon_type == 3: # epsilon is e ^ (-k / 1000) 
            self.epsilon = exp(-1 / 1000)
        elif self.epsilon_type == 4: # epsilon is e ^ (-k / 10000)
            self.epsilon = exp(-1 / 10000)
        else:
            raise ValueError("Epsilon type not understood")
        
    def get_policy(self, state):
        # hit below 12, stand above 21 always
        # no need to update n counter or q values since these are trivial states
        if state.get_sum_for_player(True) [0] < 12:
            return Action.HIT
        elif state.get_sum_for_player(True) [0] >= 21:
            return Action.STAND

        possible_actions = [action for action in Action]

        if random() < self.epsilon: # selected randomly
            chosen_action = choice(possible_actions)  
        else: # selected greedily
            q_values_by_action = {action: self.get_q_value(state.get_agent_state(), action) for action in possible_actions}

            chosen_action = max(q_values_by_action, key = q_values_by_action.get)

        self.increment_n_counter(state.get_agent_state(), chosen_action)
        self.current_episode.append((state.get_agent_state(), chosen_action))

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

        # updating the epsilon value
        if self.epsilon_type == 1:
            self.epsilon = 0.1
        elif self.epsilon_type == 2: # epsilon is 1 / k
            self.epsilon = 1 / self.episode_count
        elif self.epsilon_type == 3: # epsilon is e ^ (-k / 1000) 
            self.epsilon = exp(-self.episode_count / 1000)
        elif self.epsilon_type == 4: # epsilon is e ^ (-k / 10000)
            self.epsilon = exp(-self.episode_count / 10000)