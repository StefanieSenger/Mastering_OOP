import sys

from typing import Tuple, Any, NamedTuple

from mastering_oop.cards.suit import Suit

# polymorphic design:
#   - subclasses share __init__ with superclass
#   - all subclasses have identical signatures
#   - all subclasses have the same methods and attributes
#   - each subclass implement their own _points() method, but they all return the same type
#   - as a consequence, objects can be used interchangably thougout he programme


class Card:
    insure = False

    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)

    def __repr__(self) -> str:
        """string that could be used to re-build the object
        "!r" refers to the __repr__ of the suit and rank objects"""
        return f"{self.__class__.__name__}(suit={self.suit!r}, rank={self.rank!r})"

    def __str__(self) -> str:
        """human readable"""
        return f"{self.rank}{self.suit}"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "":
            return str(self)
        rs = (
            format_spec.replace("%r", self.rank)
            .replace("%s", self.suit)
            .replace("%%", "%")
        )
        return rs


class AceCard(Card):
    insure = True

    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):

    def _points(self) -> Tuple[int, int]:
        return 10, 10


class AceCardHashed(AceCard):
    insure = True

    def _points(self) -> Tuple[int, int]:
        return 1, 11

    def __hash__(self) -> int:
        """hash is calculated based on the objects data:
        objects with the same data now return the same hash value"""
        return (hash(self.suit) + 4 * hash(self.rank)) % sys.hash_info.modulus

    def __eq__(self, other: Any) -> bool:
        return self.suit == other.suit and self.rank == other.rank


class CardWithBytes(Card):

    def __bytes__(self) -> bytes:
        """encodes CardWithBytes into bytes from string"""
        class_code = self.__class__.__name__[0]
        rank_number_str = {"A": "1", "J": "11", "Q": "12", "K": "13"}.get(
            self.rank, self.rank
        )
        string = f"({" ".join([class_code, rank_number_str, self.suit])})"
        return bytes(string, encoding="utf-8")


class CardWithComparisons(Card):
    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, CardWithComparisons):
            return NotImplemented
        return self.rank < other.rank

    def __le__(self, other: Any) -> bool:
        try:
            return self.rank <= other.rank
        except AttributeError:
            return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, CardWithComparisons):
            return NotImplemented
        return self.rank > other.rank

    def __ge__(self, other: Any) -> bool:
        try:
            return self.rank >= other.rank
        except AttributeError:
            return NotImplemented

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CardWithComparisons):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, CardWithComparisons):
            return NotImplemented
        return self.rank != other.rank or self.suit != other.suit


class AceCardUnmutable(NamedTuple):
    """Class's __setattr__ method prevents attribues from being set."""

    rank: str  # rank attrubute doesn't hold a value: need to be specified in object initiation
    suit: Suit  ## suit attrubute doesn't hold a value: need to be specified in object initiation
    hard: int = 1
    soft: int = 11

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"


"""print("############### Try Out ###############")
cards = [AceCard('A', '♠'), Card('2','♠'), FaceCard('J','♠'),]
print(cards)"""
