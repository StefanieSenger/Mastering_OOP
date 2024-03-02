from enum import Enum
from typing import Type, List

# using Enum class:
#   - number of attributes must be finite
#   - member names are Python identifiers
#   - member values are Python objects


class Suit(str, Enum):
    """mixin class `str` is first here, so its methods can be overwritten by the Enum class if necessary"""
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class EnumDomain:
    """mixin class that adds a domain() method"""
    @classmethod
    def domain(cls: Type) -> List[str]:
        """lists all the values from the class"""
        return [m.value for m in cls]


class SuitD(str, EnumDomain, Enum):
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


"""print("############### Try Out ###############")
print(Suit.Club)
print(Suit.Heart.value)

# The class lacks in __init__ and cannot be instantiated this way. We can only access its attributes.
try:
    suit_obj = Suit()
except TypeError as e:
    print(e)


try:
    some_special_suit = Suit.Diamond()
except TypeError as e:
    print(e)

print(f"This is because `Suit.Diamond` already is an object of the Suit class, see: \
{Suit.Diamond.__class__} and {isinstance(Suit.Diamond, Suit)}")

print(list(Suit))

# The Enum attributes are immutable:
try:
    Suit.Heart.value = 'H'
except AttributeError as e:
    print(e)

# class is iterable:
print(hasattr(Suit, "__iter__"))


# mixins and multiple inheritance
print(SuitD.__mro__)
print(SuitD.domain())"""
