class NeverBuyPlayer(Player):
    buy_property = modify_buy(Player.buy_property)