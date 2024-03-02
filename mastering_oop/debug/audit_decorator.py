import logging, sys
import functools
from typing import Callable, TypeVar, List, Any, cast

from mastering_oop.cards.card_polymorphic import Card, AceCard, FaceCard
from mastering_oop.cards.deck import DeckExtended
from mastering_oop.cards.suit import Suit


# defining the type hints for mypy
FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def audit(method: F) -> F:
    """method decorator that records any state change in stateful classes,
    used to decorate setter methods"""

    @functools.wraps(method)
    def wrapper(self, *args, **kw):
        template = "%s\n     before %s\n     after %s"
        audit_log = logging.getLogger("audit")
        before = repr(self)  # a kind of deep copy to preserve state
        try:
            result = method(self, *args, **kw)
        except Exception as e:
            after = repr(self)
            audit_log.exception(template, method.__qualname__, before, after)
            raise
        after = repr(self)
        audit_log.info(template, method.__qualname__, before, after)
        return result

    return cast(F, wrapper)


print("############### Try Out ###############")

class Hand:

    def __init__(self, *cards: Card) -> None:
        self._cards = list(cards)

    @audit
    def __iadd__(self, card: Card) -> "Hand":
        self._cards.append(card)
        return self

    def __repr__(self) -> str:
        cards = ", ".join(map(str, self._cards))
        return f"{self.__class__.__name__}({cards})"


def make_cards_with_factory_function(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)
    raise Exception("Design Failure")


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
d = DeckExtended(func=make_cards_with_factory_function)
h = Hand(d.pop(), d.pop())
h += d.pop
