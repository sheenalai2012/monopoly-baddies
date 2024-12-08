from monosim.player import Player
from monosim.board import get_board, get_roads, get_properties, get_community_chest_cards, get_bank
from monosim.random_player import RandomPlayer
from monosim.always_buy_player import AlwaysBuyPlayer
from monosim.gamestate import GameState
from monosim.mcts_player import MCTSPlayer

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

    player1 = RandomPlayer('player1', 1, bank, list_board, dict_roads, dict_properties, community_cards_deck)
    agent = MCTSPlayer('agent', 2, bank, list_board, dict_roads, dict_properties, community_cards_deck)

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

        while not any(p.has_lost() for p in list_players) and round_count < 1000:
            prev_cash = agent._cash

            for player in list_players:
                if player._name == "agent":
                    # perform action
                    action = agent.play((None))
                   
                else:
                    player.play((None))

            round_count += 1

        print(f"Game #: {seed} Amount of Rounds played: {round_count} \n")
        print(f"Resulting cash player1: ${player1._cash} ")
        print(f"Resulting cash agent: ${agent._cash} \n")

        if player1._cash > agent._cash:
            player1_win_counts += 1
        else:
            player2_win_counts += 1
        
        print(f"Score {player1_win_counts}-{player2_win_counts} \n")

    
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
