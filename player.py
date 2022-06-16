from bet_strategy import BetStrategy


class Player:
    def __init__(self, start_balance: int = 1000, bet_strategy: BetStrategy = BetStrategy.BET_2_1_3):
        self.balance = start_balance
        self.bet_strategy = bet_strategy
        self.last_bet = None
        self.recent_win = False

    def bet(self) -> int:
        if self.bet_strategy == BetStrategy.BET_2_1_3:
            if not self.last_bet:
                bet = 10
            elif self.last_bet == 10:
                return 5
            elif self.last_bet > 10:
                return self.last_bet + 5
        else:
            raise NotImplementedError()

    def update_game_results(self, bet_amount: int, won: bool):
        self.last_bet = bet_amount
