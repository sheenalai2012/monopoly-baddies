import random
from monosim.player import Player

def modify_choose_action(choose_action):
    def _wrapper(self, available_actions, state):
        ans = always_buy(available_actions)
        return ans
    return _wrapper

class AlwaysBuyPlayer(Player):
    choose_action = modify_choose_action(Player.choose_action)

def always_buy(available_actions) -> str:
    if len(available_actions) == 1: # can only do nothing; return nothing
        return available_actions[0]
    if available_actions[1] == 'buy_property': # always buy property if landed on property
        return available_actions[1]
    else:
        randy = random.randint(1, len(available_actions) - 1)
        return available_actions[randy] # randomly buy house/hotel