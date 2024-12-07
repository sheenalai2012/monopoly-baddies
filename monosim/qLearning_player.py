import random
from monosim.player import Player
from monosim.random_player import choose_random_action
import pandas as pd


#def QlearningPlayer(Player):
'''
def modify_choose_action(choose_action):
    def _wrapper(self, available_actions):
        if len(available_actions) == 1: # can only do nothing; return nothing
            return available_actions[0]
        state = self.get_state()
        epsilon = .01
        action = self.qLearning_choose_action(state,available_actions,epsilon)
        return action
    return _wrapper
'''
def import_csv(filename):
    df = pd.read_csv(filename)
    df['Agent_Properties_Before'] = df['Agent_Properties_Before'].astype(str)
    df['Opponent_Properties_Before'] = df['Opponent_Properties_Before'].astype(str)
    df['Agent_Properties_After'] = df['Agent_Properties_After'].astype(str)
    df['Opponent_Properties_After'] = df['Opponent_Properties_After'].astype(str)
    df['Opponent_Properties_After'] = df['Opponent_Properties_After'].astype(str)
    df['Available_Actions'] = df['Available_Actions'].astype(str)


    return df


def read_csv(df):
    # gathers state, action, reward and next state from csv training file
    transitions = []
    for _, row in df.iterrows():
        agent_properties_before = () if row['Agent_Properties_Before'] == 'nan' else tuple(sorted(row['Agent_Properties_Before'].split('_')))
        opponent_properties_before = () if row['Opponent_Properties_Before'] == 'nan' else tuple(sorted(row['Opponent_Properties_Before'].split('_')))
        state = (
            row['Agent_Cash_Before'],
            row['Agent_Location_Before'],
            agent_properties_before,
            row['Opponent_Cash_Before'],
            opponent_properties_before,
        )

        action = row['Action']
        reward = row['Reward']

        agent_properties_after = () if row['Agent_Properties_After'] == 'nan' else tuple(sorted(row['Agent_Properties_After'].split('_')))
        opponent_properties_after = () if row['Opponent_Properties_After'] == 'nan' else tuple(sorted(row['Opponent_Properties_After'].split('_')))
        next_state = (
            row['Agent_Cash_After'],
            row['Agent_Location_After'],
            agent_properties_after,
            row['Opponent_Cash_After'],
            row['Opponent_Location_After'],
            opponent_properties_after
        )
        available_actions = tuple(row['Available_Actions'].split('_'))

        transitions.append((state, action, reward, next_state, available_actions))
    return transitions


class QLearningPlayer(Player):
    def __init__(self, name, player_id, bank, list_board, dict_roads, dict_properties, community_chest_deck, alpha=0.1, gamma=0.9, epsilon = 0.1):
        super().__init__(name, player_id, bank, list_board, dict_roads, dict_properties, community_chest_deck)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_values = {}  # Initialize Q-values storage

    def train(self):
        df = import_csv('monopoly_game_state.csv')
        transitions = read_csv(df)
        for state, action, reward, next_state, available_actions in transitions:
            self.update_q_value(state, action, reward, next_state, available_actions)
   
    def get_state(self):
        return (self._cash, self._position, tuple(sorted(self._list_owned_roads + self._list_owned_stations + self._list_owned_utilities)))
   
    def update_q_value(self, state, action, reward, next_state, next_available_actions):
    # Get the current Q-value for the (state, action) pair, initialize to 0 if no value
        current_q_value = self.q_values.get((state, action), 0)


    # Compute the maximum Q-value
        max_next_q_value = 0
        for next_action in next_available_actions:
            cur_q_value = self.q_values.get((next_state, next_action), 0)  # Default Q-value is 0
            if cur_q_value > max_next_q_value:
                max_next_q_value = cur_q_value


    # Apply the Q-learning formula to update the Q-value (Formula 17.10 from textbook)
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * max_next_q_value - current_q_value)
        self.q_values[(state, action)] = new_q_value


    def choose_action(self, available_actions, state):
        my_state, opp_state = state
        # take a random action if random value < epsilon, otherwise we take max q value     
        aMax = available_actions[0]

        tuple_state = (my_state['cash'], my_state['location'], tuple(sorted(my_state['properties'].split('_'))), opp_state['cash'], opp_state['location'], tuple(sorted(opp_state['properties'].split('_'))))
        
        vMax = self.q_values.get((tuple_state, aMax), 0)  # Default Q-value is 0
        for action in available_actions:
            curV = self.q_values.get((tuple_state, action), 0)
            if curV > vMax:
                vMax = curV
                aMax = action

        if vMax == 0:
            return choose_random_action(available_actions)

        return aMax
   
       



