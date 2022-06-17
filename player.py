import logging

import simple_strategy
from bet_strategy import BetStrategy
from hand import Hand
from simple_strategy import BetAction


class Player:
    def __init__(self, start_balance: int = 1000, bet_strategy: BetStrategy = BetStrategy.BET_2_1_3):
        self._balance = start_balance
        self.bet_strategy = bet_strategy
        self.last_bet = None
        self.recent_win = False
        self.hands_won = 0
        self.hands_lost = 0
        self.hands_push = 0

    def place_bet(self) -> int:
        if self.bet_strategy == BetStrategy.BET_2_1_3:

            bet = None

            if not self.recent_win:
                bet = 10

            if self.recent_win:
                # Player won last round
                if self.last_bet == 10:
                    bet = 5
                elif self.last_bet == 5:
                    bet = 15
                else:
                    bet = self.last_bet + 5

            # logging.debug(f"Player is betting amount {bet} (last bet: {self.last_bet} won: {self.recent_win})")
            if bet > self.balance:
                return 0

            self.last_bet = bet

            return bet

        else:
            raise NotImplementedError()

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        if new_balance > self._balance:
            self.hands_won += 1
            self.recent_win = True
        elif new_balance < self._balance:
            self.hands_lost += 1
            self.recent_win = False
        else:
            # Do nothing since we want to keep the last recent win state in a push
            self.hands_push += 1
            pass

        self._balance = new_balance
        logging.debug(f"New player balance is {self._balance}")

    def play_hand(self, hand: Hand, dealer_card: int) -> BetAction:
        logging.debug(f"Player is playing hand {hand} against dealer {dealer_card}")
        if hand.is_splittable():
            if simple_strategy.SIMPLE_STRATEGY[simple_strategy.StrategyIndex.SPLIT][hand.cards[0]][dealer_card]:
                return simple_strategy.BetAction.SPLIT

        if hand.is_soft():
            return simple_strategy.SIMPLE_STRATEGY[simple_strategy.StrategyIndex.SOFT][hand.sum()][dealer_card]

        return simple_strategy.SIMPLE_STRATEGY[simple_strategy.StrategyIndex.HARD][hand.sum()][dealer_card]

    def update_game_results(self, bet_amount: int, won: bool):
        self.last_bet = bet_amount
