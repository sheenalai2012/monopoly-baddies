import random
from monosim.player import Player

def choose_random_action(available_actions):
    diff_actions = 1
    has_house_hotel_action = False
    if len(available_actions) > 1:
        diff_actions += 1
        if available_actions[1] == 'buy_property':
            if len(available_actions) > 2:
                diff_actions += 1
                has_house_hotel_action = True
        else:
            has_house_hotel_action = True
        
    # we want to sample equally do nothing, buy property, and buy house/hotel out of max 3 that exist
    randy = random.randint(0, diff_actions - 1)
    if randy == 0: # return nothing
        return available_actions[0]
    if randy == 1 and not has_house_hotel_action: # return buy property
        return available_actions[1]

    # otherwise we sample randomly from the buy house/hotel options
    start_idx = 1 if diff_actions == 2 else 2
    randy = random.randint(start_idx, len(available_actions) - 1)
    return available_actions[randy]


def modify_choose_action(choose_action):
    def _wrapper(self, available_actions, state):
        return choose_random_action(available_actions)
        
    return _wrapper

class RandomPlayer(Player):
    choose_action = modify_choose_action(Player.choose_action)