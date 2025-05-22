
# SARSAMAX

# lets get staarted!!

from Blackjack.Agent.Agent import Agent
from Blackjack.Action import Action
from random import choice, random

from math import exp

class QLearningOffPolicyAgent(Agent):
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
        if state ["agent_sum"] < 12:
            return Action.HIT
        elif state ["agent_sum"] >=21:
            return Action.STAND
        
        possible_actions = list(Action)
        # ε-greedy action
        if random() < self.epsilon:
            action = choice(possible_actions)
        else:
            q_vals = {a: self.get_q_value(state, a) for a in possible_actions}
            action = max(q_vals, key = q_vals.get)

        self.increment_n_counter(state, action)
        self.current_episode.append((state, action))

        return action
    
    def update_agent(self, next_state, reward):
        # getting last (s, a)
        if not self.current_episode:
            return
        
        prev_state, prev_action = self.current_episode[-1]
        alpha = 1 / (self.get_n_count(prev_state, prev_action)+1)

        # finding max 
        next_state = next_state.get_agent_state()
        max_q_next = max([self.get_q_value(next_state, a) for a in Action])

        prev_q =  self.get_q_value(prev_state, prev_action)
        new_q = prev_q + alpha * ((reward if reward is not None else 0) + max_q_next - prev_q)
        self.update_q_value(prev_state, prev_action, new_q)

    def end_episode(self):
        self.episode_count +=1
        self.current_episode = []
        self.epsilon = self.compute_epsilon()