from mastering_oop.cards.card_polymorphic import Card, AceCard, FaceCard
from mastering_oop.cards.suit import Suit

# Factory Class:
#   - the goal is to have an object of type class returned
#   - the rank() method updates the constructor of the Card/AceCard/FaceCard class to match the correct rank
#   - the suit() method adds the correct suit to the constructor and creates the object


class CardFactory:

    def rank(self, rank: int) -> "CardFactory":
        """updates the state of the constructor"""

        self.class_, self.rank_str = {
            1: (AceCard, "A"),
            11: (FaceCard, "J"),
            12: (FaceCard, "Q"),
            13: (FaceCard, "K"),
        }.get(rank, (Card, str(rank)))

        return self

    def suit(self, suit: Suit) -> Card:
        """creates final Card object"""

        return self.class_(self.rank_str, suit)


"""print("############### Try Out ###############")

factory = CardFactory()
card1 = factory.rank(2).suit(Suit.Heart)

print(card1)
print(card1.__dict__)

deck = [factory.rank(r + 1).suit(s) for r in range(13) for s in Suit]
print(len(deck))
"""
