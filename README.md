# ARI2204: Reinforcement Learning Assignment

<b>Team 6: Alison Attard, Ben Taliana and Michael Farrugia</b>

## System Requirements

- Python 3.11 or higher
    - Matplotlib
    - Plotly
    - Pandas

## Structure

Our project is structured as follows, within the `Blackjack` folder:

- Game logic is implemented through the files `Round.py`, `Deck.py`, `Card.py`, `Dealer.py`, and `Action.py`.
- Agents are found within the `Agent` folder:
    - `Agent.py` contains the base class for agents.
    - `BaselineAgent.py` implements a simple agent that plays randomly.
    - `MonteCarloOnPolicyAgent.py` implements a Monte Carlo on-policy agent.
    - `SarsaOnPolicyAgent.py` implements a SARSA on-policy agent.
    - `QLearningOffPolicyAgent.py` implements a Q-learning off-policy agent.
    - `DoubleQOffPolicyAgent.py` implements a Double Q-learning off-policy agent.

## Running the Program

To play a game against the dealer, run `play_game.py`. This allows you to interactively play a game of Blackjack against the dealer, validating the game logic.

To view the results of the agent evaluation, refer to `agent_evaluation.ipynb`. This notebook contains each agent configuration's evaluation, including necessary graphs and tables.
