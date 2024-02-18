from typing import cast, Iterable, Iterator

from mastering_oop.cards.card_polymorphic import (
    Card,
    AceCard,
    FaceCard,
    AceCardHashed,
    CardWithBytes,
    CardWithComparisons,
)
from mastering_oop.cards.suit import Suit
from mastering_oop.cards.deck import DeckWrapped, DeckExtended, DeckDesigned
from mastering_oop.hands.hand import Hand, HandWithSurrogateConstructor, FrozenHand
from mastering_oop.strategies.strategy import Flat, GameStrategy
from mastering_oop.strategies.player import Player
from mastering_oop.strategies.table import Table


def make_cards_from_cards_polymorphic():
    cards = [
        AceCard("A", Suit.Spade),
        Card("2", Suit.Spade),
        FaceCard("Q", Suit.Spade),
    ]

    for card in cards:
        print(card)

    print(cards[0].__dict__)


make_cards_from_cards_polymorphic()


def make_cards_with_factory_function(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)
    raise Exception("Design Failure")


deck = [
    make_cards_with_factory_function(rank, suit)
    for rank in range(1, 14)
    for suit in Suit
]


def get_cards_from_deck():
    """uses DeckWrapped"""
    deck = DeckWrapped(func=make_cards_with_factory_function)
    hand = [deck.pop(), deck.pop()]
    return hand


def get_cards_from_deck():
    """uses DeckExtended"""
    deck = DeckExtended(func=make_cards_with_factory_function)
    hand = [deck.pop(), deck.pop()]
    return hand


def get_cards_from_deck():
    """uses DeckDesigned"""
    deck = DeckDesigned(func=make_cards_with_factory_function, decks=2)
    hand = [deck.pop(), deck.pop()]
    return hand


popped_cards = get_cards_from_deck()
print(popped_cards)
print(popped_cards[0])


def get_hand():
    """gets Hand class"""
    deck = DeckExtended(func=make_cards_with_factory_function)
    hand = Hand(deck.pop(), deck.pop(), deck.pop())
    return hand


def get_hand():
    """gets HandWithSurrogateConstructor class"""
    deck = DeckExtended(func=make_cards_with_factory_function)
    hand = HandWithSurrogateConstructor(deck.pop(), deck.pop(), deck.pop())
    return hand


hand = get_hand()
print(f"hand: {hand}")
if isinstance(hand, HandWithSurrogateConstructor):
    deck = DeckExtended(func=make_cards_with_factory_function)
    hand0, hand1 = hand.split(hand, deck.pop(), deck.pop())
    print(f"hand0: {hand0}")
    print(f"hand1: {hand1}")
print(
    f"The player has the following cards in their hands: {hand.cards}. Their hand looks like that: {hand:%r%s}."
)


def play_the_game():
    table = Table(func=make_cards_with_factory_function)
    flat_bet = Flat()
    dumb_strategy = GameStrategy()
    player = Player(table, flat_bet, dumb_strategy)
    return player


player = play_the_game()
player.game()


# immutable AceCard objects WITHOUT __hash__ and __eq__ defined:
c1 = AceCard(1, Suit.Club)
c2 = AceCard(1, Suit.Club)
print(id(c1), id(c2))  # different ids
print(c1 is c2)  # `is` is based on ids
# default hash values compute directly from the id numbers, using modulo depending on architecture: they repeat
# default hash values only exist, unless a __eq__ is created, then the object becomes unhashable, until a __hash__ is implemented as well
print(hash(c1), hash(c2))
print(
    c1 == c2
)  # for `==` to return `True`, all values must be equal, including the hash

# immutable AceCardHashed objects WITH __hash__ and __eq__ defined:
c1 = AceCardHashed(1, Suit.Club)
c2 = AceCardHashed(1, Suit.Club)
print(id(c1), id(c2))  # still different ids
print(c1 is c2)  # still separate objects in the memory
print(hash(c1), hash(c2))  # same hash value, because __hash__ is implemented
print(c1 == c2)  # results to `True`, because __eq__ is implemented to compare the data


def get_hand():
    """gets Hand class"""
    deck = DeckExtended(func=make_cards_with_factory_function)
    hand = Hand(deck.pop(), deck.pop(), deck.pop())
    frozenhand = FrozenHand(hand)
    return frozenhand


frozenhand = get_hand()
print(frozenhand)

from collections import defaultdict

stats = defaultdict(int)
stats[
    frozenhand
] += 1  # FrozenHand objects can be used as dictionary keys, since they implement __hash__
print(stats)


def check_if_empty_deck():
    if deck:
        print("deck is not empty")
    else:
        print("deck is empty")


deck = DeckExtended(func=make_cards_with_factory_function)

# way to reduce elements from the deck, without raising IndexError
check_if_empty_deck()
while deck:  # check if deck is not empty
    card = deck.pop()
check_if_empty_deck()


def card_from_bytes(buffer: bytes) -> CardWithBytes:
    """Parses bytes to rebuild the original CardWithBytes instance."""
    string = buffer.decode("utf8")
    try:
        if not (string[0] == "(" and string[-1] == ")"):
            raise ValueError
        code, rank_number, suit_value = string[1:-1].split()
        if int(rank_number) not in range(1, 14):
            raise ValueError
        return CardWithBytes(int(rank_number), Suit(suit_value))
    except (IndexError, KeyError, ValueError) as ex:
        raise ValueError(f"{buffer!r} isn't a CardWithBytes instance")


card = CardWithBytes("2", Suit.Spade)
print(card)
bytes_value = bytes(card)
print(bytes_value)
recovered_card = card_from_bytes(bytes_value)
print(recovered_card)
print(type(recovered_card))

c2 = CardWithComparisons("2", Suit.Spade)
c3 = CardWithComparisons("3", Suit.Spade)
print(c3 >= c2)
print(c3 < c2)

# comparing two hands
card_ace = AceCard(1, Suit.Heart)
card_4 = Card(4, Suit.Spade)
card_J = FaceCard("J", Suit.Diamond)
card_5 = Card(5, Suit.Club)
cards = [card_ace, card_4, card_J, card_5]

hand1 = Hand(Card(10, Suit.Spade), *cards)
print(hand1.total())  # hard total (Ace is being treated as rank '1')
# 20

card_ace = AceCard(1, Suit.Heart)
card_2 = Card(2, Suit.Spade)
card_3 = Card(3, Suit.Club)
card_3a = Card(3, Suit.Heart)
cards = [card_ace, card_2, card_3, card_3a]

hand2 = Hand(Card(10, Suit.Spade), *cards)
print(hand2.total())  # soft total (Ace is being treated as rank '11')
# 19

print(hand1 > hand2)  # 20 > 19 = True, despite the difference in hard and soft total
print(hand1 < 21)  # comparison with integer works as well

# this doesn't work with types different then Hand, because we haven't implemented a __lt__ method, only a __gt__
try:
    print(hand1 > 17)
except TypeError as e:
    print(e)


# object removal with __del__
class Noisy:

    def __del__(self) -> None:
        print(
            f"Removing {id(self)}"
        )  # see, there is no real implementation, the mere existance of __del__ does the job


obj = Noisy()
del obj  # obj gets removed, because the reference count went to 0

obj = Noisy()
another_reference = obj
del obj  # obj gets removed, whenever the total reference count of obj and another_reference goes to 0

noisy_list = [Noisy(), Noisy()]
another_reference = noisy_list[:]  # shallow copy
del noisy_list  # obj gets removed, whenever the total reference count of obj and another_reference goes to 0
del another_reference
# playing around with this hints towards how precarious thus is indeed (it's intransparent)


# Circular references and garbage collection
class Parent:

    def __init__(self, *children: "Child") -> None:
        for (
            child
        ) in (
            children
        ):  # a Parent() object references all the Child() object it contains
            child.parent = self  # this would not be the case with `from weakref import` ref and `ref(self)`
        self.children = {c.id: c for c in children}

    def __del__(self) -> None:
        print(f"Removing {self.__class__.__name__} {id(self):d}")


class Child:

    def __init__(self, id: str) -> None:
        self.id = id
        self.parent: Parent = cast(
            Parent, None
        )  # a Child() object references a Parent() object
        # this would not be the case with `from weakref import` ref and `ref(self)`

    def __del__(self) -> None:
        print(f"Removing {self.__class__.__name__} {id(self):d}")


p = Parent(Child("a"), Child("b"))
del p  # strange, all three objects actually get removed, other than stated in the textbook...

import gc

gc.collect()  # this triggers manual garbage collection for inaccessible and circular references
# (but my objects got cleaned up before anyway)


# __new__ for extending (otherwise) immutable classes to become mutable with __init__
# this does not work:
class Float_Fail(float):

    def __init__(self, value: float, unit: str) -> None:
        super().__init__(value)
        self.unit = unit


try:
    init_fails_obj = Float_Fail(value=0, unit="meter")
except TypeError as e:
    print(
        e
    )  # this does not work, since float.__init__() doesn't take  any arguments other then `self`: it's not mutable

# overriding __new__ classmethod, to make __init__ possible:


class Float_Units(float):

    def __new__(cls, value, unit):  # it also makes us a custom __init__() it seems
        obj = super().__new__(cls, float(value))
        obj.unit = unit
        return obj


speed = Float_Units(6.8, "knots")
print(speed * 2)