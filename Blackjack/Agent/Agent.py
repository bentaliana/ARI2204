class Agent:
    def __init__(self, episode):
        self.state_action_pairs = {}
        self.state_action_count = {}
        self.current_expected_value = 0
        self.episode = episode
        self.episode_count = 0

    def add_state_action_pair(self, state, action):
        if tuple(state.items()) not in self.state_action_pairs:
            self.state_action_pairs [tuple(state.items())] = []
            
        self.state_action_pairs [tuple(state.items())].append(action)
        self.__increment_state_action_count(state, action)

    def __increment_state_action_count(self, state, action):
        if tuple(state.items()) not in self.state_action_count:
            self.state_action_count [tuple(state.items())] = {} 
        
        if action not in self.state_action_count [tuple(state.items())]:
            self.state_action_count [tuple(state.items())] [action] = 0
            
        self.state_action_count [tuple(state.items())] [action] += 1

    def increment_episode_count(self):
        self.episode_count += 1

    def get_policy(self):
        pass