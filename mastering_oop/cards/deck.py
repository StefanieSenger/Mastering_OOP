import random
from typing import Optional, Type
from types import TracebackType

from mastering_oop.cards.card_polymorphic import Card, AceCard, FaceCard
from mastering_oop.cards.suit import Suit

# three ways to create a container class:
#   - wrap: surround an existing collection class (e.i. list); example of Facade design pattern
#   - extend: add functionality to existing collection class
#   - self design: build new collection class from scratch


class DeckWrapped:
    """wraps an existing collection class (a list) into a new DeckWrapped class"""

    def __init__(self, func) -> None:
        """makes a deck of cards and shuffles it"""
        self._cards = [func(rank, suit) for rank in range(1, 14) for suit in Suit]
        random.shuffle(self._cards)

    def pop(self) -> Card:
        """popping a card from a list object"""
        return self._cards.pop()


class DeckExtended(list):
    """extends to the list class, there is no need to reimplement pop(), since list
    class is already providing this method"""

    def __init__(self, func) -> None:
        """makes a deck of cards and shuffles it"""
        super().__init__(func(r + 1, s) for r in range(13) for s in Suit)
        random.shuffle(self)


class DeckDesigned(list):
    """self designed class that shuffles multiple decks and can pop a card"""

    def __init__(self, func, decks: int = 1) -> None:
        super().__init__()  # makes empty list
        for i in range(decks):
            self.extend(func(r + 1, s) for r in range(13) for s in Suit)
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()


# context manager
class DeterministicDeck:
    """Deck class with a random seed; can be used for testing and debugging.
    It's also a factory, as it creates a DeckExtended object each time it is run."""

    def __init__(self, *args, **kw) -> None:
        self.args = args
        self.kw = kw

    def __enter__(self) -> DeckExtended:
        self.was = random.getstate()
        random.seed(0, version=1) # change global configuration of random seed
        return DeckExtended(*self.args, **self.kw) # instantiate DeckExtended object

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        random.setstate(self.was) # reset global configuration of random seed
        return False


'''print("############### Try Out ###############")
# get hand from DeterministicDeck context manager
with DeterministicDeck(func=make_cards_with_factory_function) as deck:
    hand = [deck.pop(), deck.pop()] # deck with a random seed is used to make a hand

hand = [deck.pop(), deck.pop()]
print(hand) # it's always the same cards that a drawn first'''
