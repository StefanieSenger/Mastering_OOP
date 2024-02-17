from enum import Enum

# using Enum class:
#   - number of attributes must be finite
#   - attributes can be used as objects

class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


'''print("############### Try Out ###############")
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
print(hasattr(Suit, "__iter__"))'''
