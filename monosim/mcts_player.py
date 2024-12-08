import random
from monosim.player import Player
from monosim.hallucinate import MCTS

def modify_choose_action(choose_action):
    def _wrapper(self, available_actions, state):
        mcts = MCTS(self._dict_players['player1'], self)

        return mcts.select_action()
        
    return _wrapper

class MCTSPlayer(Player):
    choose_action = modify_choose_action(Player.choose_action)