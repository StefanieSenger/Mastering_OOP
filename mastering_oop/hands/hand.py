import sys
from typing import Tuple, Any, cast

from mastering_oop.cards.card_polymorphic import Card, AceCard, FaceCard
from mastering_oop.cards.deck import DeckExtended


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

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __format__(self, spec: str) -> str:
        if spec == "":
            return str(self)
        return ", ".join(f"{c:{spec}}" for c in self.cards)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() == other
        try:
            return self.cards == other.cards and self.dealer_card == other.dealer_card
        except AttributeError:
            return NotImplemented

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() < other
        try:
            return self.total() < cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() <= other
        try:
            return self.total() <= cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self.cards)
        hard = sum(c.hard for c in self.cards)
        if hard + delta_soft <= 21:
            return hard + delta_soft
        return hard


class HandWithSurrogateConstructor:
    """class offers two alternative ways to construct an instance, apart from __init__;
    the staticmethods kind of uncupple the class construction from the class,
    while still belonging to it visually"""

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    @staticmethod
    def freeze(other) -> "HandWithSurrogateConstructor":
        """creates a momemto version of the hand, similar to a frozenset"""
        hand = HandWithSurrogateConstructor(other.dealer_card, *other.cards)
        return hand

    @staticmethod
    def split(
        other, card0, card1
    ) -> Tuple["HandWithSurrogateConstructor", "HandWithSurrogateConstructor"]:
        """splits hand in two, this adheres to the rules of the blackjack game"""
        hand0 = HandWithSurrogateConstructor(other.dealer_card, other.cards[0], card0)
        hand1 = HandWithSurrogateConstructor(other.dealer_card, other.cards[1], card1)
        return hand0, hand1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.dealer_card!r}, *{self.cards})"

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __format__(self, spec: str) -> str:
        if spec == "":
            return str(self)
        return ", ".join(f"{c:{spec}}" for c in self.cards)


class FrozenHand(Hand):
    """class that freezes the state of a Hand class, attributes are not supposed to be changed
    (but are not protected against change); mimics unmutable objects"""

    def __init__(self, *args, **kw) -> None:
        if len(args) == 1 and isinstance(args[0], Hand):
            # Clone a hand
            other = cast(Hand, args[0])
            self.dealer_card = other.dealer_card
            self.cards = other.cards
        else:
            # Build a fresh Hand from Card instances.
            super().__init__(*args, **kw)

    def __hash__(self) -> int:
        """each object gets a hash value, because we play it was immutable;
        it can thus be used as a dict key or in a set"""
        return sum(hash(c) for c in self.cards) % sys.hash_info.modulus
