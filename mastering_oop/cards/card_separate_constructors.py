from mastering_oop.cards.suit import Suit

# each subclass defines their own __init__ and refers their attributes to the
# superclasses's __init__ in a unique way

class Card:

    def __init__(self, rank: str, suit: Suit, hard: int, soft: int) -> None:
        self.rank = rank
        self.suit = suit
        self.hard = hard
        self.soft = soft


class NumberCard(Card):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(str(rank), suit, rank, rank)


class AceCard(Card):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)


class FaceCard(Card):

    def __init__(self, rank: int, suit: Suit) -> None:
        rank_str = {11: "J", 12: "Q", 13: "K"}[rank]
        super().__init__(rank_str, suit, 10, 10)
