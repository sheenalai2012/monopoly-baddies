import csv
import os

class GameState:
    def __init__(self, players, csv_file='monopoly_game_state.csv'):
        self.players = players
        self.csv_file = csv_file
        self.round_counter = 0
        self.initialize_csv()

    def initialize_csv(self):
        fieldnames = [
            'Round', 
            'Agent_Cash_Before', 'Agent_Location_Before', 'Agent_Properties_Before',
            'Opponent_Cash_Before', 'Opponent_Location_Before', 'Opponent_Properties_Before',
            'Action',
            'Agent_Cash_After', 'Agent_Location_After', 'Agent_Properties_After',
            'Opponent_Cash_After', 'Opponent_Location_After', 'Opponent_Properties_After', 
            'Reward'
        ]

        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    def get_state(self, player):
        return {
            'cash': player._cash,
            'location': player._position,
            'properties': '_'.join(player._list_owned_roads + player._list_owned_stations + player._list_owned_utilities)
        }

    def log_transition(self, transition):
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(transition)