from monosim.player import Player
from monosim.board import get_board, get_roads, get_properties, get_community_chest_cards, get_bank
import random
import time 


if __name__ == '__main__':

    start_time = time.time()

    for seed in range(0, 1):
        print(seed)
        random.seed(seed)
        bank = get_bank()
        list_board, dict_roads = get_board(),  get_roads()
        dict_properties = get_properties()
        dict_community_chest_cards = get_community_chest_cards()
        community_cards_deck = list(dict_community_chest_cards.keys())
        player1 = Player('player1', 1, bank, list_board, dict_roads, dict_properties, community_cards_deck)
        agent = Player('agent', 4, bank, list_board, dict_roads, dict_properties, community_cards_deck)

        player1.meet_other_players([agent])
        agent.meet_other_players([player1])

        list_players = [agent, player1]

        idx_count = 0

        while (not agent.has_lost()) and (not player1.has_lost()) and idx_count < 100000:
            prev_cash = agent._cash

            for player in list_players:
                player.play()
                
            # reward calculation
            net_cash = agent._cash - prev_cash
            total_cash = sum(player._cash for player in list_players)

            end_game_reward = 1000000 if player1.has_lost() else 0 # 1 million bucks
            reward = (net_cash / total_cash) + end_game_reward
            print(reward)

            idx_count += 1
    print(player1._cash, agent._cash)
    print(idx_count)
 
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)