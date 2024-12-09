from copy import deepcopy
from monosim.random_player import choose_random_action
from monosim.player import Player
from monosim.always_buy_player import AlwaysBuyPlayer
from monosim.random_player import RandomPlayer

class MCTS:
    def __init__(self, player1, agent):
        self.player1 = player1
        self.agent = agent

        self.n = 100 # nunmber of rollouts for each action
    
    def select_action(self):
        available_actions = self.agent.get_available_actions()

        if len(available_actions) == 1:
            return available_actions[0]

        hallucinator = Hallucinator(self.player1, self.agent)

        max_available_action = None
        max_avg_discounted_reward = None
        for available_action in available_actions:
            avg_discounted_reward = 0
            
            for i in range(self.n):
                reward = hallucinator.random_rollout(available_action)
                avg_discounted_reward += reward

                hallucinator.reset_game_state(self.player1, self.agent)

            avg_discounted_reward /= self.n

            if max_avg_discounted_reward is None or avg_discounted_reward > max_avg_discounted_reward:
                max_avg_discounted_reward = avg_discounted_reward
                max_available_action = available_action
        
        # if len(available_actions) > 1:
        #     print(max_available_action, max_avg_discounted_reward)
        return max_available_action

class Hallucinator:
    def __init__(self, player1, agent):
        self.reset_game_state(player1, agent)

    def reset_game_state(self, player1, agent):
        bank = deepcopy(player1._bank)
        list_board = deepcopy(player1._list_board)
        dict_roads = deepcopy(player1._dict_roads)
        dict_properties = deepcopy(player1._dict_properties)
        community_cards_deck = deepcopy(player1.community_cards_deck)

        # copy over game
        self._player1 = AlwaysBuyPlayer(player1._name, player1._number, bank, list_board, dict_roads, dict_properties, community_cards_deck)
        self._agent = MCTSExplorePlayer(agent._name, agent._number, bank, list_board, dict_roads, dict_properties, community_cards_deck)

        self._player1._position = player1._position
        self._player1._dice_value = player1._dice_value
        self._player1._cash = player1._cash
        self._player1._properties_total_mortgageable_amount = player1._properties_total_mortgageable_amount
        self._player1._exit_jail = player1._exit_jail
        self._player1._jail_count = player1._jail_count
        self._player1._free_visit = player1._free_visit
        self._player1._list_owned_roads = deepcopy(player1._list_owned_roads)
        self._player1._list_owned_stations = deepcopy(player1._list_owned_stations)
        self._player1._list_owned_utilities = deepcopy(player1._list_owned_utilities)
        self._player1._list_mortgaged_roads = deepcopy(player1._list_mortgaged_roads)
        self._player1._list_mortgaged_stations = deepcopy(player1._list_mortgaged_stations)
        self._player1._list_mortgaged_utilities = deepcopy(player1._list_mortgaged_utilities)
        self._player1._dict_owned_colors = deepcopy(player1._dict_owned_colors)
        self._player1._dict_owned_houses_hotels = deepcopy(player1._dict_owned_houses_hotels)
        self._player1._has_lost = player1._has_lost
        self._player1.color_to_house_mapping = player1.color_to_house_mapping

        self._agent._position = agent._position
        self._agent._dice_value = agent._dice_value
        self._agent._cash = agent._cash
        self._agent._properties_total_mortgageable_amount = agent._properties_total_mortgageable_amount
        self._agent._exit_jail = agent._exit_jail
        self._agent._jail_count = agent._jail_count
        self._agent._free_visit = agent._free_visit
        self._agent._list_owned_roads = deepcopy(agent._list_owned_roads)
        self._agent._list_owned_stations = deepcopy(agent._list_owned_stations)
        self._agent._list_owned_utilities = deepcopy(agent._list_owned_utilities)
        self._agent._list_mortgaged_roads = deepcopy(agent._list_mortgaged_roads)
        self._agent._list_mortgaged_stations = deepcopy(agent._list_mortgaged_stations)
        self._agent._list_mortgaged_utilities = deepcopy(agent._list_mortgaged_utilities)
        self._agent._dict_owned_colors = deepcopy(agent._dict_owned_colors)
        self._agent._dict_owned_houses_hotels = deepcopy(agent._dict_owned_houses_hotels)
        self._agent._has_lost = agent._has_lost
        self._agent.color_to_house_mapping = agent.color_to_house_mapping

        self._player1.meet_other_players([self._agent])
        self._agent.meet_other_players([self._player1])


        self.gamma = 0.95
    

    def random_rollout(self, action):
        list_players = [self._agent, self._player1]
        discounted_reward = 0

        for i in range(100): # 10 turns
            prev_cash = self._agent._cash

            for player in list_players:
                if player._name == "agent":
                    if i == 0:
                        self._agent.play((), specified_action=action)
                    else:
                        self._agent.play(())
                else:
                    player.play((None, None))  # its chill bc we are not using qlearning for play function
                        # reward calculation
                    net_cash = self._agent._cash - prev_cash
                    total_cash = sum(p._cash for p in list_players)

                    end_game_reward = 1000000000 if self._player1.has_lost() else -1000000000 # 1 million bucks

                    if total_cash == 0:
                        reward = end_game_reward
                    else:
                        reward = (net_cash ) + end_game_reward

                    discounted_reward = self.gamma * discounted_reward + reward

                    if self._player1.has_lost() or self._agent.has_lost():
                        return discounted_reward
                        # print("inside", discounted_reward)
 
        return discounted_reward

# the exploration player
def modify_choose_action(choose_action):
    def _wrapper(self, available_actions, state):
        return choose_random_action(available_actions)
        
    return _wrapper

class MCTSExplorePlayer(Player):
    choose_action = modify_choose_action(Player.choose_action)