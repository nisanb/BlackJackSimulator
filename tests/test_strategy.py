from typing import Tuple

import pytest

from bet_strategy import BetStrategy
from hand import Hand
from player import Player
from simple_strategy import BetAction


@pytest.mark.parametrize(
    "player_hand,dealer_card,expected_result",
    [
        ((5, 6), 5, BetAction.DOUBLE),
        ((6, 5), 5, BetAction.DOUBLE),
        ((11, 10), 5, BetAction.STAND),
        ((11, 6), 6, BetAction.DOUBLE),
        ((11, 6), 7, BetAction.HIT),
        ((11, 2), 3, BetAction.HIT),
        ((11, 2), 4, BetAction.HIT),
        ((11, 2), 5, BetAction.DOUBLE),
        ((11, 11), 5, BetAction.SPLIT),
        ((10, 10), 5, BetAction.STAND),
        ((9, 9), 7, BetAction.STAND),
        ((9, 9), 8, BetAction.SPLIT),
        ((9, 9), 10, BetAction.STAND),
        ((7, 7), 8, BetAction.HIT),
        ((7, 7), 7, BetAction.SPLIT),
    ]
 )
def test_basic_strategy(player_hand: Tuple[int, int], dealer_card: int, expected_result: BetAction):
    player = Player(bet_strategy=BetStrategy.BET_2_1_3)

    hand = Hand(player, player.place_bet())
    for card in player_hand:
        hand.add_card(card)

    assert player.play_hand(hand=hand, dealer_card=dealer_card) == expected_result
