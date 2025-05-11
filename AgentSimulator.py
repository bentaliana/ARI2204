from Blackjack.Round import Round
from Blackjack.Dealer import Dealer
from Blackjack.Action import Action
from Blackjack.Agent.MonteCarloOnPolicyAgent import MonteCarloOnPolicyAgent
from Blackjack.Agent.Agent import Agent
from Blackjack.Action import Action

class AgentSimulator():
    def __init__(self, agent: Agent):
        self.agent = agent
        self.round = None

    def play_round(self):
        self.round = Round()

        action = Action.HIT

        while action == Action.HIT and self.round.get_terminal_state() is None and self.round.get_sum_for_player(True) != 21:
            action = self.agent.get_policy(self.round)

            if action == Action.HIT:
                self.round.hit()
            elif action == Action.STAND:
                self.round.stand()

        if self.round.get_terminal_state() is not None:
            self.agent.update_agent(self.round)

            return self.round.get_terminal_state(True)
        
        # Automatically stand for player if they have 21 from the start, or if they reach 21 after hitting
        if self.round.get_sum_for_player(True) == 21:
            self.round.stand() # Change turn to dealer

        dealer = Dealer()

        while dealer.get_policy(self.round.get_sum_for_player(False)) == True and self.round.get_terminal_state() == None:
            self.round.hit()

        self.agent.update_agent(self.round)

        return self.round.get_terminal_state(True)

    def simulate_games(self, num_games):
        results = {
            "wins": 0,
            "losses": 0,
            "draws": 0
        }

        for _ in range(num_games):
            result = self.play_round()

            if result == 1:
                results ["wins"] += 1
            elif result == -1:
                results ["losses"] += 1
            else:
                results ["draws"] += 1

        return results

mcop_agent_1 = MonteCarloOnPolicyAgent(True, 1)
mcop_agent_2 = MonteCarloOnPolicyAgent(False, 1)
mcop_agent_3 = MonteCarloOnPolicyAgent(False, 2)
mcop_agent_4 = MonteCarloOnPolicyAgent(False, 3)

mcop_agent_1_simulator = AgentSimulator(mcop_agent_1)
mcop_agent_2_simulator = AgentSimulator(mcop_agent_2)
mcop_agent_3_simulator = AgentSimulator(mcop_agent_3)
mcop_agent_4_simulator = AgentSimulator(mcop_agent_4)

results_agent_1 = mcop_agent_1_simulator.simulate_games(1000)
results_agent_2 = mcop_agent_2_simulator.simulate_games(1000)
results_agent_3 = mcop_agent_3_simulator.simulate_games(1000)
results_agent_4 = mcop_agent_4_simulator.simulate_games(1000)

print(results_agent_1)
print(results_agent_2)
print(results_agent_3)
print(results_agent_4)