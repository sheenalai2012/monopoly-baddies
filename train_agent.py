import pickle
from monosim.player import Player
from monosim.board import get_board, get_roads, get_properties, get_community_chest_cards, get_bank

from monosim.qLearning_player import QLearningPlayer

def save_agent(agent, filename):
    with open(filename, 'wb') as f:
        pickle.dump(agent, f)

if __name__ == '__main__':
    bank = get_bank()
    list_board, dict_roads = get_board(), get_roads()
    dict_properties = get_properties()
    dict_community_chest_cards = get_community_chest_cards()
    community_cards_deck = list(dict_community_chest_cards.keys())

    agent = QLearningPlayer('agent', 2, bank, list_board, dict_roads, dict_properties, community_cards_deck)
    
    print("Training started...")
    agent.train()  # Train the agent
    print("Training ended...")

    save_agent(agent, 'trained_agent.pkl')  # Save the trained model
    print("Agent saved!")
