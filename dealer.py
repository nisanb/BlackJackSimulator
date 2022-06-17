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
        print("====Starting New Hand====")
        hands = [Hand(player, player.place_bet()) for player in self.registered_players]

        for hand in hands:
            hand.add_card(self.deal_card())

        dealer_hand = Hand()
        dealer_hand.add_card(self.deal_card())

        for hand in hands:
            hand.add_card(self.deal_card())

        dealer_hand.add_card(self.deal_card())

        # Override scenario
        # dealer_hand = Hand()
        # dealer_hand.add_card(2)
        # dealer_hand.add_card(3)
        # hands = [Hand(self.registered_players[0], 10)]
        # hands[0].add_card(6)
        # hands[0].add_card(11)

        for hand in hands:
            if hand.is_blackjack():
                continue

            decision = None
            while decision != BetAction.STAND and not hand.is_bust():
                decision = hand.player.play_hand(hand=hand, dealer_card=dealer_hand.cards[0])
                print(f"Player chose: {decision}")

                if decision == BetAction.STAND:
                    break

                if decision == BetAction.HIT:
                    hand.add_card(self.deal_card())

                if decision == BetAction.SPLIT:
                    print("Should split but skipping for now")
                    break

                if decision == BetAction.DOUBLE:
                    hand.add_card(self.deal_card())
                    hand.bet_amount *= 2
                    print(f"Player doubled ! Only one card!")
                    print(f"{hand}")
                    break

        # All hands finished playing
        # Deal to the dealer
        # Dealer stops on soft 17
        while dealer_hand.sum() < 17:
            dealer_hand.add_card(self.deal_card())

        self.finish_round(dealer_hand=dealer_hand, player_hands=hands)

        if len(self.deck) > self.red_card:
            # Dealer should shuffle
            self.shuffle()

    def finish_round(self, dealer_hand: Hand, player_hands: List[Hand]):
        print("====Finishing Hand====")
        print(f"Dealer hand: {dealer_hand}")

        for hand in player_hands:
            print(f"Player hand: {hand}")

            if hand.is_bust():
                # Player busted
                print("Player Busted")
                hand.player.balance -= hand.bet_amount
                continue

                # With soft hand, we will alter the hand sum
                hand.cards.append(-11)

            if hand.is_blackjack():
                if dealer_hand.is_blackjack():
                    # Player push
                    print("Player and dealer both blackjack pushed")
                    hand.player.balance += 0
                    continue

                # Player wins 3 to 2
                print("Player won blackjack")
                hand.player.balance += hand.bet_amount + hand.bet_amount * 1.5
                continue

            if dealer_hand.is_bust():
                # Dealer busted, award
                print("Dealer busted")
                hand.player.balance += hand.bet_amount
                continue

            if hand.sum() == dealer_hand.sum():
                if not dealer_hand.is_blackjack():
                    print("Player pushed")
                    # Dummy placeholder just to kick things
                    hand.player.balance += 0
                    continue

                # Player lost
                print("Player lost")
                hand.player.balance -= hand.bet_amount

            if hand.sum() > dealer_hand.sum():
                print("Player won")
                hand.player.balance += hand.bet_amount
                continue

            # Player lost
            print("Player lost")
            hand.player.balance -= hand.bet_amount

        print(f"Round finished!")


if __name__ == "__main__":
    print(Game().shuffle())
