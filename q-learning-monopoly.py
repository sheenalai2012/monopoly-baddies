from monosim.player import Player
from monosim.board import get_board, get_roads, get_properties, get_community_chest_cards, get_bank
import random
import time 


if __name__ == '__main__':

    start_time = time.time()

    for seed in range(0, 1000):
        print(seed)
        random.seed(seed)
        bank = get_bank()
        list_board, dict_roads = get_board(),  get_roads()
        dict_properties = get_properties()
        dict_community_chest_cards = get_community_chest_cards()
        community_cards_deck = list(dict_community_chest_cards.keys())
        player1 = Player('player1', 1, bank, list_board, dict_roads, dict_properties, community_cards_deck)
        player2 = Player('player2', 2, bank, list_board, dict_roads, dict_properties, community_cards_deck)
        player3 = Player('player3', 3, bank, list_board, dict_roads, dict_properties, community_cards_deck)
        player4 = Player('player4', 4, bank, list_board, dict_roads, dict_properties, community_cards_deck)

        player1.meet_other_players([player2, player3, player4])
        player2.meet_other_players([player1, player3, player4])
        player3.meet_other_players([player1, player2, player4])
        player4.meet_other_players([player1, player2, player3])

        list_players = [player1, player2, player3, player4]

        idx_count = 0

        num_in_game = int(not player1._has_lost) + int(not player2._has_lost) + int(not player3._has_lost) + int(not player4._has_lost)
        while num_in_game > 1 and idx_count < 2000:
            for player in list_players:
                player.play()
            idx_count += 1
            num_in_game = int(not player1._has_lost) + int(not player2._has_lost) + int(not player3._has_lost) + int(not player4._has_lost)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)