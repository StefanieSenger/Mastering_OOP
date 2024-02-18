from mastering_oop.cards.deck import DeckExtended
from mastering_oop.hands.hand import Hand
from mastering_oop.strategies.strategy import BettingStrategy, GameStrategy


class Table:
    """tracks the state of the game"""

    def __init__(self, func) -> None:
        self.deck = DeckExtended(func=func)

    def place_bet(self, amount: int) -> None:
        print("Bet", amount)

    def get_hand(self) -> Hand:
        try:
            self.hand = Hand(self.deck.pop(), self.deck.pop(), self.deck.pop())
            self.hole_card = self.deck.pop()
        except IndexError:
            # Out of cards: need to shuffle.
            # This is not technically correct: cards currently in play should not appear in the next deck.
            self.deck = DeckExtended(func=make_cards_with_factory_function)
            return self.get_hand()
        print("Deal", self.hand)
        return self.hand

    def can_insure(self, hand: Hand) -> bool:
        return hand.dealer_card.insure
