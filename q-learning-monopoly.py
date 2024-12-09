from monosim.player import Player
from monosim.board import get_board, get_roads, get_properties, get_community_chest_cards, get_bank
from monosim.random_player import RandomPlayer
from monosim.always_buy_player import AlwaysBuyPlayer
from monosim.gamestate import GameState
from monosim.qLearning_player import QLearningPlayer
from collections import defaultdict

import pickle
import random
import time
import matplotlib.pyplot as plt
import numpy as np

def plot_win_counts(player1_win_counts, player2_win_counts):
    """Create a bar plot for player win counts."""
    categories = ['player1', 'agent']
    values = [player1_win_counts, player2_win_counts]
    
    plt.bar(categories, values)
    plt.xlabel('Players')
    plt.ylabel('Win Count')
    plt.title('Win Count for Player1 vs Agent')
    plt.show()

def plot_property_frequencies(properties_owned):
    """Create a bar plot for the frequency of owned properties."""
    names = list(properties_owned.keys())
    frequencies = list(properties_owned.values())

    plt.figure(figsize=(10, 6))
    plt.bar(names, frequencies, color='blue')

    plt.title('Frequency of Properties Owned', fontsize=16)
    plt.xlabel('Property Names', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()  
    plt.show()

def plot_action_frequencies(player_action_counts, agent_action_counts):
    # buy_property, nothing, buy_house, buy_hotel
    player_actions, agent_actions = defaultdict(int), defaultdict(int)

    for action in player_action_counts:
        if action == "nothing":
            player_actions[action] += player_action_counts[action]
        elif action == "buy_property":
            player_actions[action] += player_action_counts[action]
        alt_action= action.split("_")
        if len(alt_action) > 2:
            key = alt_action[0] + "_" + alt_action[2]
            player_actions[key] += player_action_counts[action]

    for action in agent_action_counts:
        if action == "nothing":
            agent_actions[action] += agent_action_counts[action]
        elif action == "buy_property":
            agent_actions[action] += agent_action_counts[action]
        alt_action= action.split("_")

        if len(alt_action) > 2:
            key = alt_action[0] + "_" + alt_action[2]
            agent_actions[key] += agent_action_counts[action]

    actions = list(set(player_actions.keys()).union(set(agent_actions.keys())))

    player_values = [player_actions.get(action, 0) for action in actions]
    agent_values = [agent_actions.get(action, 0) for action in actions]


    print("printing player_values: ", player_values)

    bar_width = 0.35
    values = np.arange(len(actions))

    plt.yscale('log')
    plt.bar(values, player_values, bar_width, label="Player Actions", color="red")
    plt.bar(values + bar_width, agent_values, bar_width, label="Agent Actions", color="blue")
    plt.legend()
    plt.xticks(values, actions)
    plt.show()

def gather_all_states(agent, opponent):
    agent_state = game_state.get_state(agent)
    opponent_state = game_state.get_state(opponent)
    return agent_state, opponent_state

def load_agent(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    start_time = time.time()
    print("Simulation Started...")

    properties_owned = {}
    last_owned = None

    player_action_counts, agent_action_counts = defaultdict(int), defaultdict(int)

    # just for player initialization purposes
    bank = get_bank()
    list_board, dict_roads = get_board(), get_roads()
    dict_properties = get_properties()
    dict_community_chest_cards = get_community_chest_cards()
    community_cards_deck = list(dict_community_chest_cards.keys())

    # init all properties that exist
    all_prop = dict_properties | dict_roads
    for prop in all_prop:
        properties_owned[prop] = 0

    # player1 = AlwaysBuyPlayer('player1', 1, bank, list_board, dict_roads, dict_properties, community_cards_deck)
    player1 = RandomPlayer('player1', 2, bank, list_board, dict_roads, dict_properties, community_cards_deck)
    agent = load_agent('trained_agent.pkl')

    SAVE_STATE = False

    player1_win_counts = 0
    player2_win_counts = 0
    for seed in range(0, 100): 
        random.seed(seed)
        bank = get_bank()
        list_board, dict_roads = get_board(), get_roads()
        dict_properties = get_properties()
        dict_community_chest_cards = get_community_chest_cards()
        community_cards_deck = list(dict_community_chest_cards.keys())

        player1.reset(bank, list_board, dict_roads, dict_properties, community_cards_deck)
        agent.reset(bank, list_board, dict_roads, dict_properties, community_cards_deck)

        list_players = [player1, agent]

        for player in list_players:
            player.meet_other_players([p for p in list_players if p != player])

        game_state = GameState(list_players)
        round_count = 0

        while not any(p.has_lost() for p in list_players) and round_count < 100000:
            prev_cash = agent._cash

            for player in list_players:
                # gather state before action
                prev_state, opponent_state_before = gather_all_states(agent, player1)
                if player._name == "agent":
                    
                    available_actions = '?'.join(agent.get_available_actions())
                    
                    # perform action
                    action = agent.play((prev_state, opponent_state_before))

                    if action:
                        agent_action_counts[action] += 1

                    # gather state after action
                    new_state, opponent_state_after = gather_all_states(agent, player1)

                    # reward calculation
                    net_cash = new_state['cash'] - prev_state['cash']
                    total_cash = sum(p._cash for p in list_players)

                    end_game_reward = 1000000 if player1.has_lost() else 0  # 1 million buckaroos

                    reward = end_game_reward

                    if total_cash:
                        reward = (net_cash / total_cash) + end_game_reward

                    transition = [
                        round_count,
                        prev_state['cash'],
                        prev_state['location'],
                        prev_state['properties'],
                        opponent_state_before['cash'],
                        opponent_state_before['location'],
                        opponent_state_before['properties'],
                        action,
                        new_state['cash'],
                        new_state['location'],
                        new_state['properties'],
                        opponent_state_after['cash'],
                        opponent_state_after['location'],
                        opponent_state_after['properties'],
                        reward,
                        available_actions
                    ]

                    last_owned = new_state['properties']
                    if SAVE_STATE:
                        game_state.log_transition(transition)

                else:
                    player_action = player.play((prev_state, opponent_state_before))

                    if player_action:
                        player_action_counts[player_action] += 1
            
            round_count += 1

        print(f"Game #: {seed} Amount of Rounds played: {round_count} \n")
        print(f"Resulting cash player1: ${player1._cash} ")
        print(f"Resulting cash agent: ${agent._cash} \n")

        if player1.has_lost() or agent._cash > player1._cash:
            player2_win_counts += 1

            last_owned = last_owned.split("_")
            for name in last_owned:
                properties_owned[name] += 1
            
        else:
            player1_win_counts += 1
    
    # plot_win_counts(player1_win_counts, player2_win_counts)
    # plot_property_frequencies(properties_owned)
    # plot_action_frequencies(player_action_counts, agent_action_counts)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time)


    

