from abc import abstractmethod
from collections import defaultdict

class Agent:
    def __init__(self):
        self.n_counter = defaultdict(int) # keyed using (state, action)
        self.q_values = defaultdict(float) # keyed using (state, action)
        self.episode_count = 0

    def increment_n_counter(self, state, action):
        self.n_counter [(frozenset(state.items()), action)] += 1

    def get_n_count(self, state, action):
        return self.n_counter [(frozenset(state.items()), action)]

    def update_q_value(self, state, action, value):
        self.q_values [(frozenset(state.items()), action)] = value

    def get_q_value(self, state, action):
        return self.q_values [(frozenset(state.items()), action)]
    
    @abstractmethod
    def get_policy(self, state):
        pass