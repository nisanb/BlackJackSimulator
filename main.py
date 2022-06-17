import logging

from bet_strategy import BetStrategy
from dealer import Game
from player import Player

if __name__ == "__main__":

    import matplotlib.pyplot as plt

    plt.ion()
    fig = plt.figure(figsize=(16, 8))
    axes = fig.add_subplot(111)
    data_plot = plt.plot(0, 0)
    line, = axes.plot([], [])

    game = Game(amount_of_decks=5, rounds=1)
    player = Player(start_balance=3000, bet_strategy=BetStrategy.BET_2_1_3)

    game.registered_players.append(player)

    played_hands = []
    balances = []
    while not game.play_round():
        played_hands.append(game.played_hands)
        balances.append(player.balance)
        line.set_ydata(balances)
        line.set_xdata(played_hands)
        if len(balances) > 0:
            axes.set_ylim(min(balances), max(balances) + 1)  # +1 to avoid singular transformation warning
            axes.set_xlim(min(played_hands), max(played_hands) + 1)
        plt.title(f"Total Hands: {game.played_hands} Pushed: {player.hands_push}, Won: {player.hands_won}, Lost: {player.hands_lost}")
        plt.draw()
        plt.pause(0.1)
        pass

    plt.show(block=True)
    logging.debug(f"Game finished at hand #{game.played_hands}")

