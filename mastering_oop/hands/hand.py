import sys
from typing import Tuple, Any, cast, List

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
        """splits hand in two hands, this adheres to the rules of the blackjack game"""
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


class HandLazyProperty(Hand):

    @property
    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self.cards)
        hard_total = sum(c.hard for c in self.cards)
        if hard_total + delta_soft <= 21:
            return hard_total + delta_soft
        return hard_total

    @property
    def card(self) -> List[Card]:
        return self.cards

    @card.setter
    def card(self, aCard: Card) -> None:
        self.cards.append(aCard)

    @card.deleter
    def card(self) -> None:
        self.cards.pop(-1)


class HandEagerProperty(Hand):

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.total = 0  # total is a simple attribute, that's computed eagerly as each card is added
        self._delta_soft = 0
        self._hard_total = 0
        self.cards: List[Card] = list()
        for c in cards:  # calls `card()` method wrapped into `@card.setter`
            self.card = c  # type: ignore

    @property
    def card(self) -> List[Card]:
        return self.cards

    @card.setter
    def card(self, aCard: Card) -> None:
        self.cards.append(aCard)
        self._delta_soft = max(aCard.soft - aCard.hard, self._delta_soft)
        self._hard_total = self._hard_total + aCard.hard
        self._set_total()  # calculation of total is part of setter method

    @card.deleter
    def card(self) -> None:
        removed = self.cards.pop(-1)
        self._hard_total -= removed.hard
        # Issue: was this the only ace?
        self._delta_soft = max(c.soft - c.hard for c in self.cards)
        self._set_total()  # new eager calculation of total

    def _set_total(self) -> None:
        if self._hard_total + self._delta_soft <= 21:
            self.total = self._hard_total + self._delta_soft
        else:
            self.total = self._hard_total

    def split(self, deck: DeckExtended) -> "HandEagerProperty":
        """Pop card from hand and use it to create a new hand, that is then returned."""
        assert (
            self.cards[0].rank == self.cards[1].rank
        )  # I don't know why this check is here, and mostly the code would fail withouzt propper error handeling ...
        c1 = self.cards[
            -1
        ]  # this code only works properly if we have only two cards in the HandEagerProperty() object, maybe that's the rules in blackjack ...
        del self.card  # delete last card from `self.cards` list
        self.card = deck.pop()  # add new card to `self.cards` list
        h_new = self.__class__(self.dealer_card, c1, deck.pop())
        return h_new


class HandWithContains(Hand):
    """class that implements __contains__"""

    def __contains__(self, other):
        if other in (card.rank for card in self.cards):
            return True
        return False
