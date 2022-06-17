from bet_strategy import BetStrategy
from player import Player


def test_player_betting():
    player = Player()
    if player.bet_strategy == BetStrategy.BET_2_1_3:
        assert player.place_bet() == 10

        player.recent_win = True
        player.last_bet = 10
        assert player.place_bet() == 5

        player.recent_win = False
        player.last_bet = 5
        assert player.place_bet() == 10

        player.recent_win = True
        player.last_bet = 10
        assert player.place_bet() == 5

        player.recent_win = True
        player.last_bet = 5
        assert player.place_bet() == 15

        for _ in range(20):
            last_bet = player.last_bet
            new_bet = player.place_bet()
            assert new_bet - last_bet == 5



