from typing import List

# TODO from player import Player


class Hand:
    def __init__(self, player=None, bet_amount: int = -1):
        self.player = player
        self.cards: List[int] = []
        self.bet_amount = bet_amount

    def add_card(self, card: int):
        self.cards.append(card)

    def sum(self):
        if self.is_soft() and sum(self.cards) > 21:
            return sum(self.cards)-11

        return sum(self.cards)

    def is_soft(self):
        return 11 in self.cards and sum(self.cards) < 22

    def is_bust(self):
        return self.sum() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.sum() == 21

    def is_splittable(self):
        return len(self.cards) == 2 and self.cards[0] == self.cards[1]

    def __str__(self):
        return f'{",".join((str(i) for i in self.cards))} ({self.sum()})'
