import simple_strategy
from bet_strategy import BetStrategy
from hand import Hand
from simple_strategy import BetAction


class Player:
    def __init__(self, start_balance: int = 1000, bet_strategy: BetStrategy = BetStrategy.BET_2_1_3):
        self.balance = start_balance
        self.bet_strategy = bet_strategy
        self.last_bet = None
        self.recent_win = False

    def place_bet(self) -> int:
        if self.bet_strategy == BetStrategy.BET_2_1_3:
            if not self.last_bet:
                bet = 10
            elif self.last_bet == 10:
                return 5
            elif self.last_bet > 10:
                return self.last_bet + 5
        else:
            raise NotImplementedError()

    def play_hand(self, hand: Hand, dealer_card: int) -> BetAction:
        print(f"Player is playing hand {hand} with dealer card {dealer_card}")

        if hand.is_splittable():
            if simple_strategy.SIMPLE_STRATEGY[simple_strategy.StrategyIndex.SPLIT][hand.cards[0]][dealer_card]:
                return simple_strategy.BetAction.SPLIT

        if hand.is_soft():
            return simple_strategy.SIMPLE_STRATEGY[simple_strategy.StrategyIndex.SOFT][hand.sum()][dealer_card]

        return simple_strategy.SIMPLE_STRATEGY[simple_strategy.StrategyIndex.HARD][hand.sum()][dealer_card]

    def update_game_results(self, bet_amount: int, won: bool):
        self.last_bet = bet_amount
