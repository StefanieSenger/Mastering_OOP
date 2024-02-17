from mastering_oop.cards.card_polymorphic import Card, AceCard, FaceCard

class Hand:

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def card_append(self, card: Card) -> None:
        self.cards.append(card)

    def hard_total(self) -> int:
        return sum(c.hard for c in self.cards)

    def soft_total(self) -> int:
        return sum(c.soft for c in self.cards)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.dealer_card!r}, *{self.cards})"
