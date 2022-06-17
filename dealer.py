import logging
import random
from typing import List

from hand import Hand
from player import Player
from simple_strategy import BetAction


class Game:
    def __init__(self, amount_of_decks: int = 5, rounds: int = 1):
        self.amount_of_decks = amount_of_decks
        self.deck = []
        self.hands = []
        self.red_card: int = None
        self.rounds = rounds
        self.registered_players: List[Player] = list()
        self.shuffle()
        self.played_hands = 0

    def shuffle(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * self.amount_of_decks
        random.shuffle(self.deck)
        self.red_card = random.randint(150, 200)

    def deal_card(self):
        return self.deck.pop()

    def play_round(self) -> bool:
        if self.played_hands >= self.rounds:
            # Game Finished
            return True
        self.played_hands += 1
        logging.debug("====Starting New Hand====")
        hands: List[Hand] = list()
        for player in self.registered_players:
            bet = player.place_bet()
            if bet == 0:
                # Player has no more money!
                self.registered_players.remove(player)
                continue
            hands.append(Hand(player, bet))

        if not self.registered_players:
            logging.debug("All players finished!")
            return True

        for hand in hands:
            hand.add_card(self.deal_card())

        dealer_hand = Hand()
        dealer_hand.add_card(self.deal_card())

        for hand in hands:
            hand.add_card(self.deal_card())

        dealer_hand.add_card(self.deal_card())

        # Override scenario
        dealer_hand = Hand()
        dealer_hand.add_card(5)
        dealer_hand.add_card(10)
        hands = [Hand(self.registered_players[0], 10)]
        hands[0].add_card(8)
        hands[0].add_card(8)

        played_hands: List[Hand] = list()

        while hands:
            hand = hands.pop(0)

            split_hand = False
            decision = None
            while decision != BetAction.STAND and not hand.is_bust():
                if hand.is_blackjack():
                    continue

                decision = hand.player.play_hand(hand=hand, dealer_card=dealer_hand.cards[0])
                logging.debug(f"Player chose: {decision}")

                if decision == BetAction.STAND:
                    break

                if decision == BetAction.HIT:
                    hand.add_card(self.deal_card())

                if decision == BetAction.SPLIT:
                    # Remove the hand
                    split_hand = True
                    splitted_card = hand.cards[0]
                    for i in range(2):
                        hand = Hand(player=hand.player, bet_amount=hand.bet_amount)
                        hand.add_card(splitted_card)
                        hand.add_card(self.deal_card())
                        hands.insert(0, hand)
                    break

                if decision == BetAction.DOUBLE:
                    hand.add_card(self.deal_card())
                    hand.bet_amount *= 2
                    logging.debug(f"Player doubled ! Only one card!")
                    logging.debug(f"{hand}")
                    break

            if not split_hand:
                played_hands.append(hand)

        # All hands finished playing
        # Deal to the dealer
        # Dealer stops on soft 17
        while dealer_hand.sum() < 17:
            dealer_hand.add_card(self.deal_card())

        self.finish_round(dealer_hand=dealer_hand, player_hands=played_hands)

        if len(self.deck) > self.red_card:
            # Dealer should shuffle
            self.shuffle()

    def finish_round(self, dealer_hand: Hand, player_hands: List[Hand]):
        logging.debug("====Finishing Hand====")
        logging.debug(f"Dealer hand: {dealer_hand}")

        for hand in player_hands:
            logging.debug(f"Player hand: {hand}")

            if hand.is_bust():
                # Player busted
                logging.debug("Player Busted")
                hand.player.balance -= hand.bet_amount
                continue

                # With soft hand, we will alter the hand sum
                hand.cards.append(-11)

            if hand.is_blackjack():
                if dealer_hand.is_blackjack():
                    # Player push
                    logging.debug("Player and dealer both blackjack pushed")
                    hand.player.balance += 0
                    continue

                # Player wins 3 to 2
                logging.debug("Player won blackjack")
                hand.player.balance += hand.bet_amount + hand.bet_amount * 1.5
                continue

            if dealer_hand.is_bust():
                # Dealer busted, award
                logging.debug("Dealer busted")
                hand.player.balance += hand.bet_amount
                continue

            if hand.sum() == dealer_hand.sum():
                if not dealer_hand.is_blackjack():
                    logging.debug("Player pushed")
                    # Dummy placeholder just to kick things
                    hand.player.balance += 0
                    continue

                # Player lost
                logging.debug("Player lost")
                hand.player.balance -= hand.bet_amount

            if hand.sum() > dealer_hand.sum():
                logging.debug("Player won")
                hand.player.balance += hand.bet_amount
                continue

            # Player lost
            logging.debug("Player lost")
            hand.player.balance -= hand.bet_amount

        logging.debug(f"Round finished!")


if __name__ == "__main__":
    logging.debug(Game().shuffle())
