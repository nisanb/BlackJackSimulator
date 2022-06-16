from bet_strategy import BetStrategy
from dealer import Game
from player import Player

if __name__ == "__main__":
    game = Game(amount_of_decks=5, rounds=1)
    player = Player(start_balance=1000, bet_strategy=BetStrategy.BET_2_1_3)

    game.registered_players.append(player)

    game.play_round()

    pass