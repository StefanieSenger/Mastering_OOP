from typing import cast, Iterable, Iterator

from mastering_oop.cards.card_polymorphic import Card, AceCard, FaceCard
from mastering_oop.cards.suit import Suit
from mastering_oop.cards.deck import DeckWrapped, DeckExtended, DeckDesigned
from mastering_oop.hands.hand import Hand

def make_cards_from_cards_polymorphic():
    cards = [AceCard('A', Suit.Spade), Card('2', Suit.Spade), FaceCard('Q', Suit.Spade),]

    for card in cards:
        print(card)

    print(cards[0].__dict__)

# make_cards_from_cards_polymorphic()


def make_cards_with_factory_function(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J", 12: "Q", 13: "K"}[rank]
        return FaceCard(name, suit)
    raise Exception("Design Failure")

# deck = [make_cards_with_factory_function(rank, suit) for rank in range(1, 14) for suit in Suit]

def get_cards_from_deck():
    '''uses DeckWrapped'''
    deck = DeckWrapped(func=make_cards_with_factory_function)
    hand = [deck.pop(), deck.pop()]
    return hand

def get_cards_from_deck():
    '''uses DeckExtended'''
    deck = DeckExtended(func=make_cards_with_factory_function)
    hand = [deck.pop(), deck.pop()]
    return hand

def get_cards_from_deck():
    '''uses DeckDesigned'''
    deck = DeckDesigned(func=make_cards_with_factory_function, decks=2)
    hand = [deck.pop(), deck.pop()]
    return hand

#popped_cards = get_cards_from_deck()
#print(popped_cards)
#print(popped_cards[0])

def get_hand():
    deck = DeckExtended(func=make_cards_with_factory_function)
    hand = Hand(deck.pop(), deck.pop(), deck.pop())
    return hand

print(get_hand())
