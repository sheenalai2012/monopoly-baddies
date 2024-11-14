from monosim.player import Player
from monosim.board import get_board, get_roads, get_properties, get_community_chest_cards, get_bank


if __name__ == '__main__':
    import random
    for seed in range(0, 1):
        random.seed(seed)
        bank = get_bank()
        list_board, dict_roads = get_board(),  get_roads()
        dict_properties = get_properties()
        dict_community_chest_cards = get_community_chest_cards()
        community_cards_deck = list(dict_community_chest_cards.keys())
        player1 = Player('player1', 1, bank, list_board, dict_roads, dict_properties, community_cards_deck)
        player2 = Player('player2', 2, bank, list_board, dict_roads, dict_properties, community_cards_deck)

        player1.meet_other_players([player2])
        player2.meet_other_players([player1])

        list_players = [player1, player2]

        idx_count = 0
        while not player1.has_lost() and not player2.has_lost() and idx_count < 2000:
            for player in list_players:
                player.play()
            idx_count += 1
        print("player1", player1._has_lost)
        print("player2", player2._has_lost)
        print(idx_count)