from typing import Tuple

# polymorphic design:
#   - subclasses share __init__ with superclass
#   - all subclasses have identical signatures
#   - all subclasses have the same methods and attributes
#   - each subclass implement their own _points() method, but they all return the same type
#   - as a consequence, objects can be used interchangably thougout he programme

class Card:

    def __init__(self, rank: str, suit: str) -> None:
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]:
        return int(self.rank), int(self.rank)

    def __str__(self):
        return str(self.__dict__)


class AceCard(Card):

    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):

    def _points(self) -> Tuple[int, int]:
        return 10, 10


'''print("############### Try Out ###############")
cards = [AceCard('A', '♠'), Card('2','♠'), FaceCard('J','♠'),]
print(cards)'''
