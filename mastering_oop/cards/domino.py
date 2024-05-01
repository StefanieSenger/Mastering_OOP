# this file shows the advantages of SOLID design principles

import random
from typing import Tuple, List, Iterator, Optional, Type, NamedTuple


class DominoBoneYard:
    """
    A relatively poor design. A number of unrelated things all jumbled
    together

    >>> random.seed(42)
    >>> dby = DominoBoneYard()
    >>> len(dby._dominoes)
    28
    >>> hands = list(dby.hand_iter(4))
    >>> hands[0]
    [(5, 3), (5, 1), (4, 0), (6, 0), (6, 6), (3, 0), (2, 2)]
    >>> dby.score_hand(hands[0])
    43
    >>> hands[1]
    [(4, 1), (4, 4), (3, 3), (6, 3), (4, 2), (5, 4), (5, 0)]
    >>> dby.rank_hand(hands[1])
    >>> dby.score_hand(hands[1][-2:])
    10
    >>> hands[2]
    [(6, 4), (1, 0), (4, 3), (1, 1), (5, 2), (6, 5), (2, 1)]
    >>> dby.doubles_indices(hands[0])
    [4, 6]
    >>> for d in  dby.doubles_indices(hands[0]):
    ...     print(hands[0][d])
    (6, 6)
    (2, 2)
    >>> dby.can_play_first(hands[0])
    True
    """

    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [(x, y) for x in range(limit + 1) for y in range(x + 1)]
        random.shuffle(self._dominoes)

    def double(self, domino: Tuple[int, int]) -> bool:
        x, y = domino
        return x == y

    def score(self, domino: Tuple[int, int]) -> int:
        return domino[0] + domino[1]

    def hand_iter(self, players: int = 4) -> Iterator[List[Tuple[int, int]]]:
        for p in range(players):
            yield self._dominoes[p * 7:p * 7 + 7]

    def can_play_first(self, hand: List[Tuple[int, int]]) -> bool:
        for d in hand:
            if self.double(d) and d[0] == 6:
                return True
        return False

    def score_hand(self, hand: List[Tuple[int, int]]) -> int:
        return sum(d[0] + d[1] for d in hand)

    def rank_hand(self, hand: List[Tuple[int, int]]) -> None:
        hand.sort(key=self.score, reverse=True)

    def doubles_indices(self, hand: List[Tuple[int, int]]) -> List[int]:
        return [i for i in range(len(hand)) if self.double(hand[i])]


# Interface Segregation Principle:
# segregating the code into classes that make sense to the problem and to possible extensions

class Domino(NamedTuple):
    v1: int
    v2: int

    def double(self) -> bool:
        return self.v1 == self.v2

    def score(self) -> int:
        return self.v1 + self.v2


class Hand(list):

    def score(self) -> int:
        return sum(d.score() for d in self)

    def rank(self) -> None:
        self.sort(key=lambda d: d.score(), reverse=True)

    def doubles_indices(self) -> List[int]:
        return [i for i in range(len(self)) if self[i].double()]


class DominoBoneYard2:

    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [Domino(x, y) for x in range(limit + 1) for y in range(x + 1)]
        random.shuffle(self._dominoes)

    def hand_iter(self, players: int = 4) -> Iterator[Hand]:
        for p in range(players):
            hand, self._dominoes = Hand(self._dominoes[:7]), self._dominoes[7:]
            yield hand

# Open Closed Principle
# this class is a variation of DominoBoneYard2 that allows for easy extension

class DominoBoneYard3b:

    hand_size: int = 7

    def __init__(self, limit: int = 6) -> None:
        self._dominoes = [Domino(x, y) for x in range(limit + 1) for y in range(x + 1)]
        random.shuffle(self._dominoes)

    def hand_iter(self, players: int = 4) -> Iterator[Hand]:
        for p in range(players):
            hand = Hand(self._dominoes[:self.hand_size])
            self._dominoes = self._dominoes[self.hand_size:]
            yield hand


print("############### Try Out ###############")

dominoe_set = DominoBoneYard2()
hands = list(dominoe_set.hand_iter(players=4))
print(hands)

print(dominoe_set._dominoes)

print(type(hands[0]))
print(hands[0])
hands[0].sort()
print(hands[0].score())

dominoe_set = DominoBoneYard3b()
hands = list(dominoe_set.hand_iter(players=4))
print(hands)