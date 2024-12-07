from monosim.player import Player
from monosim.board import get_board, get_roads, get_properties, get_community_chest_cards, get_bank
from monosim.random_player import RandomPlayer
from monosim.always_buy_player import AlwaysBuyPlayer
from monosim.gamestate import GameState
from monosim.qLearning_player import QLearningPlayer

import random
import time
import matplotlib.pyplot as plt


def gather_all_states(agent, opponent):
    agent_state = game_state.get_state(agent)
    opponent_state = game_state.get_state(opponent)
    return agent_state, opponent_state

if __name__ == '__main__':
    start_time = time.time()

    # just for player initialization purposes
    bank = get_bank()
    list_board, dict_roads = get_board(), get_roads()
    dict_properties = get_properties()
    dict_community_chest_cards = get_community_chest_cards()
    community_cards_deck = list(dict_community_chest_cards.keys())

    player1 = AlwaysBuyPlayer('player1', 1, bank, list_board, dict_roads, dict_properties, community_cards_deck)
    # agent = RandomPlayer('agent', 2, bank, list_board, dict_roads, dict_properties, community_cards_deck)
    agent = QLearningPlayer('agent', 2, bank, list_board, dict_roads, dict_properties, community_cards_deck)
    agent.train()


    player1_win_counts = 0
    player2_win_counts = 0
    for seed in range(0, 1000): 
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
                    

                    # perform action
                    action = agent.play((prev_state, opponent_state_before))

                    # gather state after action
                    new_state, opponent_state_after = gather_all_states(agent, player1)

                    # reward calculation
                    net_cash = new_state['cash'] - prev_state['cash']
                    total_cash = sum(p._cash for p in list_players)

                    end_game_reward = 1000000 if player1.has_lost() else 0  # 1 million bucks
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
                        reward
                    ]
                    # game_state.log_transition(transition)
                else:
                    player.play((prev_state, opponent_state_before))

            round_count += 1

        print(f"Game #: {seed} Amount of Rounds played: {round_count} \n")
        print(f"Resulting cash player1: ${player1._cash} ")
        print(f"Resulting cash agent: ${agent._cash} \n")

        if player1.has_lost():
            player2_win_counts += 1
        else:
            player1_win_counts += 1
    
    # make a graph
    categories = ['player1', 'agent']
    values = [player1_win_counts, player2_win_counts]
    plt.bar(categories, values)
    plt.xlabel('Players')
    plt.ylabel('Win Count')
    plt.title('Win Count for Player1 vs Agent')
    plt.show()
    


    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time)
