import abc
from abc import abstractmethod

from mastering_oop.hands.hand import Hand

# these classes often follow the strategy design pattern, meaning:
# data is provided as method arguments and the classes store
# very little data themselves, sometimes they are even stateless


class GameStrategy:

    def insurance(self, hand: Hand) -> bool:
        return False

    def split(self, hand: Hand) -> bool:
        return False

    def double(self, hand: Hand) -> bool:
        return False

    def hit(self, hand: Hand) -> bool:
        return sum(c.hard for c in hand.cards) <= 17


class BettingStrategy:

    def bet(self) -> int:
        raise NotImplementedError("No bet method")

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass


class BettingStrategy2(metaclass=abc.ABCMeta):

    @abstractmethod
    def bet(self) -> int:
        pass

    def record_win(self):
        pass

    def record_loss(self):
        pass


class Flat(BettingStrategy):

    def bet(self) -> int:
        return 1

print("############### Try Out ###############")
