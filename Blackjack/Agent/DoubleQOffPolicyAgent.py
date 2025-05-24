from Blackjack.Agent.Agent import Agent
from Blackjack.Action import Action

from random import choice, random
from collections import defaultdict
from math import exp

class DoubleQOffPolicyAgent(Agent):
    def __init__ (self,epsilon_type):
        super().__init__()

        self.episode_count = 1
        self.current_episode = []
        self.epsilon_type = epsilon_type
        self.epsilon = self.compute_epsilon()

        self.q1_values = defaultdict(float)
        self.q2_values = defaultdict(float)

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
      
    def update_q1_value(self, state, action, value):
        self.q1_values [(frozenset(state.items()), action)] = value
        
    def update_q2_value(self, state, action, value):
        self.q2_values [(frozenset(state.items()), action)] = value
        
    def get_q1_value(self, state, action):
        return self.q1_values [(frozenset(state.items()), action)]
        
    def get_q2_value(self, state, action):
        return self.q2_values [(frozenset(state.items()), action)]

    def get_q_value(self, state, action):
        q1 = self.get_q1_value(state, action)
        q2 = self.get_q2_value(state, action)

        return (q1 + q2) / 2
    
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
    
    def update_agent(self, next_state, reward):
        if not self.current_episode:
            return

        reward = 0 if reward is None else reward

        prev_state, prev_action = self.current_episode[-1]
        alpha = 1 / (self.get_n_count(prev_state, prev_action) + 1)
        
        next_state = next_state.get_agent_state()

        if random() < 0.5:
            q1_values_next = {a: self.get_q1_value(next_state, a) for a in Action}
            a_max = max(q1_values_next, key = q1_values_next.get)
            next_q = self.get_q2_value(next_state, a_max)

            prev_q = self.get_q1_value(prev_state, prev_action)
            new_q = prev_q + alpha * (reward + next_q - prev_q)
            self.update_q1_value(prev_state, prev_action, new_q)
        else:
            q2_values_next = {a: self.get_q2_value(next_state, a) for a in Action}
            a_max = max(q2_values_next, key = q2_values_next.get)
            next_q = self.get_q1_value(next_state, a_max)

            prev_q = self.get_q2_value(prev_state, prev_action)
            new_q = prev_q + alpha * (reward + next_q - prev_q)
            self.update_q2_value(prev_state, prev_action, new_q)

    def end_episode(self):
        self.episode_count += 1
        self.current_episode = []
        self.epsilon = self.compute_epsilon()