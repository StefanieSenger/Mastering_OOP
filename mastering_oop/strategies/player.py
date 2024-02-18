from mastering_oop.strategies.table import Table
from mastering_oop.strategies.strategy import BettingStrategy, GameStrategy

# how a player can interact with the table


class Player:

    def __init__(
        self, table: Table, bet_strategy: BettingStrategy, game_strategy: GameStrategy
    ) -> None:
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table = table

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
        if self.table.can_insure(self.hand):
            if self.game_strategy.insurance(self.hand):
                self.table.insure(self.bet_strategy.bet())
