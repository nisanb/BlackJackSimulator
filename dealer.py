import random
from typing import List

from hand import Hand
from player import Player
from simple_strategy import BetAction


class Game:
    def __init__(self, amount_of_decks: int = 5, rounds: int = 1):
        self.amount_of_decks = 5
        self.deck = []
        self.hands = []
        self.red_card: int = None
        self.rounds = rounds
        self.registered_players: List[Player] = list()
        self.shuffle()

    def shuffle(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * self.amount_of_decks
        random.shuffle(self.deck)
        self.red_card = random.randint(150, 200)

    def deal_card(self):
        return self.deck.pop()

    def play_round(self):

        hands = [Hand(player) for player in self.registered_players]

        for hand in hands:
            hand.add_card(self.deal_card())

        dealer1 = self.deal_card()

        for hand in hands:
            hand.add_card(self.deal_card())

        dealer2 = self.deal_card()

        for hand in hands:
            print(f"Player is playing hand: {hand}")
            if hand.is_blackjack():
                continue

            decision = None
            while decision != BetAction.STAND and not hand.is_bust():
                decision = hand.player.play_hand(hand=hand, dealer_card=dealer1)
                print(decision)

                if decision == BetAction.STAND:
                    break

                if decision == BetAction.HIT:
                    hand.add_card(self.deal_card())

                if decision == BetAction.SPLIT:
                    print("Should split but skipping for now")
                    break

                if decision == BetAction.DOUBLE:
                    hand.add_card(self.deal_card())
                    print(f"Player doubled ! Only one card!")
                    print(f"{hand}")
                    break

        if len(self.deck) > self.red_card:
            # Dealer should shuffle
            self.shuffle()


if __name__ == "__main__":
    print(Game().shuffle())