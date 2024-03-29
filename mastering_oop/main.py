from typing import cast, Iterable, Iterator, Optional, Any, Type, DefaultDict, List, Tuple, Dict, Union
from types import TracebackType
from dataclasses import dataclass, FrozenInstanceError
import random
import numbers
import math
from collections import Counter
from pathlib import Path

from mastering_oop.cards.card_polymorphic import (
    Card,
    AceCard,
    FaceCard,
    AceCardHashed,
    CardWithBytes,
    CardWithComparisons,
    AceCardUnmutable,
)
from mastering_oop.cards.suit import Suit
from mastering_oop.cards.deck import DeckWrapped, DeckExtended, DeckDesigned, DeterministicDeck
from mastering_oop.hands.hand import (
    Hand,
    HandWithSurrogateConstructor,
    FrozenHand,
    HandLazyProperty,
    HandEagerProperty,
    HandWithContains,
)
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


# overwriting __new__ classmethod, to make __init__ possible:
class Float_Units(float):

    def __new__(cls, value, unit):  # it also makes us a custom __init__() it seems
        obj = super().__new__(cls, float(value))
        obj.unit = unit
        return obj


speed = Float_Units(6.8, "knots")
print(speed * 2)


deck = DeckExtended(func=make_cards_with_factory_function)
cards = [deck.pop(), deck.pop(), deck.pop()]

# testing lazy property handling by HandLazyProperty()
hand = HandLazyProperty(Card(10, Suit.Spade), *cards)
print(
    hand.total
)  # total is a method, but appears like a property; recalculated every time, but only uppon request

hand.card = (
    deck.pop()
)  # card can be updated as is it was an attribute, but in fact the card() method is run
print(hand.total)

print(hand.card)  # see property

# testing eager property with HandEagerProperty()
hand = HandEagerProperty(Card(10, Suit.Spade), *cards)
print(
    hand.total
)  # total is a method, but appears like a property; recalculated every time, but only upon request

deck = DeckExtended(func=make_cards_with_factory_function)
hand.card = (
    deck.pop()
)  # card can be updated as is it was an attribute, but in fact the card() method is run
print(hand.total)

print(hand.card)  # see property


# test HandEagerProperty.split()
# we can only split if the two cards are of equal rank
hand_to_split = HandEagerProperty(
    Card(10, Suit.Spade), *(Card(2, Suit.Spade), Card(2, Suit.Club))
)

new_hand = hand_to_split.split(deck)
print(f"new_hand: {new_hand}")
print(f"old hand: {hand_to_split}")


# test AceCardUnmutable() for mutability
unmutable_card = AceCardUnmutable(suit=Suit.Club, rank=11)
print(unmutable_card.suit)  # we can get an attribute
print(unmutable_card.rank)

# but we cannot set an attribute
try:
    unmutable_card.hard = 12
except AttributeError as e:
    print(e)

# and we cannot create any new attribute
try:
    unmutable_card.new_attribute = "This is an ambiguous card."
except AttributeError as e:
    print(e)


# dataclass provides __post_init__ method
@dataclass
class RateTimeDistance:
    """Computes any of three values, when the other two are given.
    Internally __getattr__ is being called whenever the computed attribute does not exist.
    """

    rate: Optional[float] = None
    time: Optional[float] = None
    distance: Optional[float] = None

    def __post_init__(self) -> None:
        """Calculates values immediately after __init__ is run, similar to a @property decorated attribute."""
        if self.rate is not None and self.time is not None:
            self.distance = self.rate * self.time
        elif self.rate is not None and self.distance is not None:
            self.time = self.distance / self.rate
        elif self.time is not None and self.distance is not None:
            self.rate = self.distance / self.time


very_smart_calculator = RateTimeDistance(distance=1000, time=10)
print(very_smart_calculator)
very_smart_calculator.distance = 3.14
print(very_smart_calculator)  # not so smart output


# we can freeze this class, so it behaves like a NamedTuple (immutable)
@dataclass(frozen=True)
class FrozenRateTimeDistance:
    """Computes any of three values, when the other two are given and provides immutable data."""

    rate: Optional[float] = None
    time: Optional[float] = None
    distance: Optional[float] = None

    def __post_init__(self) -> None:
        """Calculates values immediately after __init__ is run, similar to a @property decorated attribute."""
        if self.rate is not None and self.time is not None:
            # self.distance = self.rate * self.time # can't be set directly with frozen=True
            object.__setattr__(self, "distance", self.rate * self.time)
        elif self.rate is not None and self.distance is not None:
            # self.time = self.distance / self.rate # can't be set directly with frozen=True
            object.__setattr__(self, "time", self.distance / self.rate)
        elif self.time is not None and self.distance is not None:
            # self.rate = self.distance / self.time # can't be set directly with frozen=True
            object.__setattr__(self, "rate", self.distance / self.time)


very_smart_calculator = FrozenRateTimeDistance(time=1, rate=0)
print(very_smart_calculator)
try:
    very_smart_calculator.distance = 100
except FrozenInstanceError as e:
    print(e)  # smarter output: the usual __setattr__() method raises an Error


# __getattribute__()
class SuperSecret:
    """Prevents access to attributes starting with an underscore."""

    def __init__(self, hidden: Any, exposed: Any) -> None:
        self._hidden = hidden
        self.exposed = exposed

    def some_custom_method():
        pass

    def __getattribute__(self, item: str):
        """overwritten, so that not any attribute from __dict__ is returned, but the
        ones starting with a single `_` are excluded."""
        if len(item) >= 2 and item[0] == "_" and item[1] != "_":
            raise AttributeError(item)
        return super().__getattribute__(item)


secret = SuperSecret(hidden="password", exposed="user_name")
try:
    secret._hidden
except AttributeError as e:
    print(f"AttributeError: {e}")  # not very verbose, but maybe enough

# __dir__() and __dict__ will still reveal the existence of `_hidden`, since here they come with their default implementation
print(secret.__dir__())
print(secret.__dict__)


@dataclass
class RTD:
    rate: Optional[float]
    time: Optional[float]
    distance: Optional[float]

    def compute(self) -> "RTD":
        if self.distance is None and self.rate is not None and self.time is not None:
            self.distance = self.rate * self.time
        elif self.rate is None and self.distance is not None and self.time is not None:
            self.rate = self.distance / self.time
        elif self.time is None and self.distance is not None and self.rate is not None:
            self.time = self.distance / self.rate
        return self


r = RTD(distance=13.5, rate=6.1, time=None)
print(r.compute())
print(dir(r))


# implementation of a callable class
class Power():

    def __call__(self, x: int, n: int) -> int:
        p = 1
        for i in range(n):
            p *= x
        return p

power = Power()
print(power(2, 3))


# or by inheritance
from collections.abc import Callable
class Power(Callable):

    def __call__(self, x: int, n: int) -> int:
        """implementing this is still expected (will raise a specific error message if we forget)"""
        p = 1
        for i in range(n):
            p *= x
        return p

power = Power()
print(power(2, 3))


# optimized power callable with an algorithm (O(log_2_n)) and a cache for memoization
class OptimizedPower:

    def __init__(self) -> None:
        self.memo: Dict[int, int] = {}

    def __call__(self, x: int, n: int) -> int:
        if (x, n) not in self.memo:
            if n == 0:
                self.memo[x, n] = 1
            elif n % 2 == 1:
                self.memo[x, n] = self.__call__(x, n - 1) * x
            elif n % 2 == 0:
                t = self.__call__(x, n // 2)
                self.memo[x, n] = t * t
            else:
                raise Exception("Logic Error")
        return self.memo[x, n]

power = OptimizedPower()
print(power(2, 134))
print(power.memo)


# context manager with global change to random number generator
class KnownSequence:
    """context manager that changes the global seed of random"""

    def __init__(self, seed: int = 0) -> None:
        self.seed = seed

    def __enter__(self) -> 'KnownSequence':
        self.was = random.getstate() # saves previous state of random
        random.seed(self.seed, version=1) # changes state of random to new value
        return self # returning self is common for mixin context managers

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]], # exceptions that raise are passed into __exit__
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType]
    ) -> Optional[bool]:
        random.setstate(self.was) # sets state of random back to previous state

        # if we return False or any object with `bool(obj)==False`, then the exceptions will raise if they exist;
        # returning True or alike will silence the exceptions
        return False

print(f"random numbers without seed: {tuple(random.randint(0, 10) for i in range(10))}") # differs

with KnownSequence() as fixed_random_state:
    #print(fixed_random_state.seed)
    #print(fixed_random_state.was)
    print(f"random numbers fixed seed: {tuple(random.randint(0, 10) for i in range(10))}") # always the same


# get hand from DeterministicDeck context manager
with DeterministicDeck(func=make_cards_with_factory_function) as deck:
    hand = [deck.pop(), deck.pop()] # deck with a random seed is used to make a hand

hand = Hand(deck.pop(), deck.pop(), deck.pop())
print(hand) # it's always the same cards that a drawn first


# the Hand class uses a list for the cards attribute and we can iterate through the list to find an Ace:
deck = DeckExtended(func=make_cards_with_factory_function)
hand = Hand(deck.pop(), deck.pop(), deck.pop())
print(type(hand))
print(hand.cards)

# we can search the list serially:
print(any(card.rank == "A" for card in hand.cards))

# this also works, because Hand.cards implements `__contains__`
print("A" in hand.cards)
print(dir(hand.cards))
print("__contains__" in dir(hand.cards)) # <--- this!

# this does not work, because the Hand() object itself does not implement `__contains__`
try:
    print("A" in hand)
except TypeError as e:
    print(e)

# this works, because HandWithContains implements `__contains__`
hand = HandWithContains(deck.pop(), deck.pop(), deck.pop())
print(hand.cards)
print("A" in hand)


# using DefaultDict for making keys
def dice_examples(n: int=12, seed: Any=None) -> DefaultDict[int, List]:
    """generates examples of dice rolls and accumulates them into a dictionary where the
    keys represent the possible outcomes of rolling two six-sided dice, the values are
    lists of tuples representing individual dice rolls."""
    if seed:
        random.seed(seed)
    Roll = Tuple[int, int]
    outcomes: DefaultDict[int, List[Roll]] = defaultdict(list) # defaultdict with empty list as a default for any key (existing or not)
    for _ in range(n):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        # `outcomes` is a DefaultDict with the key d1+d2 and the values being a list of tuples containing d1 and d2
        outcomes[d1+d2].append((d1, d2)) # if the key already exists, value tuple is simply appended
    return outcomes

print(dice_examples())
print(dice_examples()[10])
print(dice_examples()['bla']) # defaults to an empty list


# try the same thing with a usual dict
def dice_examples(n: int=12, seed: Any=None) -> Dict:
    if seed:
        random.seed(seed)
    Roll = Tuple[int, int]
    outcomes: dict[int, List[Roll]] = dict()
    for _ in range(n):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        outcomes[d1+d2].append((d1, d2)) # <-- KeyError here, because this key is not existing in the dict
    return outcomes

try:
    print(dice_examples())
except KeyError as e:
    print(f"KeyError: {e}")


# playing with Counter() objects
counter1 = Counter("hsejvoelejajaja")
print(f"counter1: {counter1}")
counter2 = Counter("wwhjnxnalaaadfffcdvevbjejvbe")
print(f"counter2: {counter2}")

# we can compute union and intersection:
print(counter1+counter2)
print(counter1-counter2)


# tracing which numeric operants are used
'''import sys

def trace(frame, event, arg):
    if frame.f_code.co_name.startswith("__"):
        print(f"frame.f_code.co_name: {frame.f_code.co_name},\nframe.f_code.co_filename: {frame.f_code.co_filename},\nevent: {event}")

sys.settrace(trace) # now everything we run passes through our trace function'''

class NoisyFloat(float):

    def __add__(self, other: float) -> 'NoisyFloat':
        print(self, "+", other)
        return NoisyFloat(super().__add__(other))

    def __radd__(self, other: float) -> 'NoisyFloat':
        print(self, "r+", other)
        return NoisyFloat(super().__radd__(other))

num1 = NoisyFloat(12)

num1+0.3
0.5+num1


# defining our own number class
class FixedPoint(numbers.Rational):
    """class of scaled numbers, that contain an integer value and a scaling factor;
    can be used for currency conversion;
    we need to implement quite a few methods to satisfy the requirements of the abstract base class"""
    __slots__ = ("value", "scale", "default_format")

    def __init__(self, value: Union['FixedPoint', int, float], scale: int = 100) -> None:
        self.value: int
        self.scale: int
        if isinstance(value, FixedPoint):
            self.value = value.value
            self.scale = value.scale
        elif isinstance(value, int):
            self.value = value
            self.scale = scale
        elif isinstance(value, float):
            self.value = int(scale * value + .5)  # Round half up
            self.scale = scale
        else:
            raise TypeError(f"Can't build FixedPoint from {value!r} of {type(value)}")
        digits = int(math.log10(scale))
        self.default_format = "{{0:.{digits}f}}".format(digits=digits)

    def __str__(self) -> str:
        return self.__format__(self.default_format)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__:s}({self.value:d},scale={self.scale:d})"

    def __format__(self, specification: str) -> str:
        if specification == "":
            specification = self.default_format
        return specification.format(self.value / self.scale)  # no rounding

    def numerator(self) -> int:
        return self.value

    def denominator(self) -> int:
        return self.scale

    def __add__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value + other * self.scale
        else:
            new_scale = max(self.scale, other.scale)
            new_value = self.value * (new_scale // self.scale) + other.value * (
                new_scale // other.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __sub__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value - other * self.scale
        else:
            new_scale = max(self.scale, other.scale)
            new_value = self.value * (new_scale // self.scale) - other.value * (
                new_scale // other.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __mul__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = self.value * other
        else:
            new_scale = self.scale * other.scale
            new_value = self.value * other.value
        return FixedPoint(int(new_value), scale=new_scale)

    def __truediv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = int(self.value / other)
        else:
            new_value = int(self.value / (other.value / other.scale))
        return FixedPoint(new_value, scale=self.scale)

    def __floordiv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = int(self.value // other)
        else:
            new_value = int(self.value // (other.value / other.scale))
        return FixedPoint(new_value, scale=self.scale)

    def __mod__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = (self.value / self.scale) % other
        else:
            new_value = self.value % (other.value / other.scale)
        return FixedPoint(new_value, scale=self.scale)

    def __pow__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = (self.value / self.scale) ** other
        else:
            new_value = (self.value / self.scale) ** (other.value / other.scale)
        return FixedPoint(int(new_value) * self.scale, scale=self.scale)

    def __abs__(self) -> 'FixedPoint':
        return FixedPoint(abs(self.value), self.scale)

    def __float__(self) -> float:
        return self.value / self.scale

    def __int__(self) -> int:
        return int(self.value / self.scale)

    def __trunc__(self) -> int:
        return int(math.trunc(self.value / self.scale))

    def __ceil__(self) -> int:
        return int(math.ceil(self.value / self.scale))

    def __floor__(self) -> int:
        return int(math.floor(self.value / self.scale))

    # reveal_type(numbers.Rational.__round__)

    def __round__(self, ndigits: Optional[int] = 0) -> Any:
        return FixedPoint(round(self.value / self.scale, ndigits=ndigits), self.scale)

    def __neg__(self) -> 'FixedPoint':
        return FixedPoint(-self.value, self.scale)

    def __pos__(self) -> 'FixedPoint':
        return self

    def __radd__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = other * self.scale + self.value
        else:
            new_scale = max(self.scale, other.scale)
            new_value = other.value * (new_scale // other.scale) + self.value * (
                new_scale // self.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __rsub__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = other * self.scale - self.value
        else:
            new_scale = max(self.scale, other.scale)
            new_value = other.value * (new_scale // other.scale) - self.value * (
                new_scale // self.scale
            )
        return FixedPoint(int(new_value), scale=new_scale)

    def __rmul__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_scale = self.scale
            new_value = other * self.value
        else:
            new_scale = self.scale * other.scale
            new_value = other.value * self.value
        return FixedPoint(int(new_value), scale=new_scale)

    def __rtruediv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = self.scale * int(other / (self.value / self.scale))
        else:
            new_value = int((other.value / other.scale) / self.value)
        return FixedPoint(new_value, scale=self.scale)

    def __rfloordiv__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = self.scale * int(other // (self.value / self.scale))
        else:
            new_value = int((other.value / other.scale) // self.value)
        return FixedPoint(new_value, scale=self.scale)

    def __rmod__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = other % (self.value / self.scale)
        else:
            new_value = (other.value / other.scale) % (self.value / self.scale)
        return FixedPoint(new_value, scale=self.scale)

    def __rpow__(self, other: Union['FixedPoint', int]) -> 'FixedPoint':
        if not isinstance(other, FixedPoint):
            new_value = other ** (self.value / self.scale)
        else:
            new_value = (other.value / other.scale) ** self.value / self.scale
        return FixedPoint(int(new_value) * self.scale, scale=self.scale)

    def __eq__(self, other: Any) -> bool:
        """equality tests involving floats should never be written with `==` (because of imprecisions),
        but rather with `abs(a-b)/a <= eps`, with `eps` being a small value that we define here;
        allowing Any type here is a requirement from the abstract method from the abstract superclass"""
        if isinstance(other, FixedPoint):
            if self.scale == other.scale:
                return self.value == other.value
            else:
                return self.value * other.scale // self.scale == other.value
        else:
            return abs(self.value / self.scale - float(other)) < .5 / self.scale

    def __ne__(self, other: Any) -> bool:
        return not (self == other) # I wonder why this is so lax, compared to __equ__
        # and I wonder it this makes objects being equal and not equal at the same time ...

    def __le__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale <= float(other)

    def __lt__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale < float(other)

    def __ge__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale >= float(other)

    def __gt__(self, other: 'FixedPoint') -> bool:
        return self.value / self.scale > float(other)

    def __hash__(self) -> int:
        """from the Python doc section 4.4.4 for implementing a hash for a two part numeric type"""
        P = sys.hash_info.modulus
        m, n = self.value, self.scale
        # Remove common factors of P; unnecessary if m and n already coprime.
        while m % P == n % P == 0:
            m, n = m // P, n // P # now m and n are coprimes (at least one is a prime and the other is not a factor of it)

        if n % P == 0:
            hash_ = sys.hash_info.inf
        else:
            # Fermat's Little Theorem: pow(n, P-1, P) is 1, so
            # pow(n, P-2, P) gives the inverse of n modulo P.
            hash_ = (abs(m) % P) * pow(n, P - 2, P) % P
        if m < 0:
            hash_ = -hash_
        if hash_ == -1:
            hash_ = -2
        return hash_

    def round_to(self, new_scale: int) -> 'FixedPoint':
        f = new_scale / self.scale
        return FixedPoint(int(self.value * f + .5), scale=new_scale)

fixed_point_number = FixedPoint(value=99, scale=100)
print(fixed_point_number)

other_fixed_point_number = FixedPoint(value=990, scale=1000)
print(other_fixed_point_number)

# since we have implemented __eq__ in that way and allowed those numbers to have the same hash value,
# this should result in "True", but it doesn't, which is confusing
print(fixed_point_number is other_fixed_point_number)


# attributes of a function
def f():
    "docstring of f, accessed by f.__doc__"
    pass

print(f.__name__)
print(f.__doc__)
print(f.__module__)
print(f.__qualname__)


# staticmethod decorator
class Angle(float):
    __slots__ = ("_degrees",)

    @staticmethod
    def from_radians(value: float) -> "Angle":
        return Angle(180 * value / math.pi)

    def __init__(self, degrees: float) -> None:
        self._degrees = degrees

    @property
    def radians(self) -> float:
        return math.pi * self._degrees / 180

    @property
    def degrees(self) -> float:
        return self._degrees

a = Angle(22.5)
print(round(a.radians/math.pi, 3))

b = Angle.from_radians(.227)
print(round(b.degrees, 1))

b.radians

try:
    b.radians = 60
except AttributeError as e:
    print(e)


def location_list(config_name: str = "someapp.config") -> List[Path]:
    """Find locations of configuration files."""
    config_locations = (
        Path(__file__),
        # Path("~someapp").expanduser(), if a special username
        Path("/opt") / "someapp",
        Path("/etc") / "someapp",
        Path.home(),
        Path.cwd(),
    )
    candidates = (dir / config_name for dir in config_locations)
    config_paths = [path for path in candidates if path.exists()]
    return config_paths

print(location_list("code"))
print(location_list("docker"))
print(location_list("Python"))
