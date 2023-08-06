import random
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import NewType, Tuple, Type

RoomID = NewType("RoomID", uuid.UUID)
"""
A unique ID of a poker room.
"""

PlayerID = str
"""
A unique ID of a poker player in a `Room`.
"""

PlayerAgentAddress = NewType("PlayerAgentAddress", str)
"""
An IP address of a poker player agent.
"""

NumChips = int
"""
A number of chips.
"""

RandomSeed = int | float | str | bytes | bytearray | None
"""
A seed value for a pseudo-random number generator.
"""


@unique
class Card(Enum):
    CLUBS_2 = auto()
    CLUBS_3 = auto()
    CLUBS_4 = auto()
    CLUBS_5 = auto()
    CLUBS_6 = auto()
    CLUBS_7 = auto()
    CLUBS_8 = auto()
    CLUBS_9 = auto()
    CLUBS_10 = auto()
    CLUBS_JACK = auto()
    CLUBS_QUEEN = auto()
    CLUBS_KING = auto()
    CLUBS_ACE = auto()
    DIAMONDS_2 = auto()
    DIAMONDS_3 = auto()
    DIAMONDS_4 = auto()
    DIAMONDS_5 = auto()
    DIAMONDS_6 = auto()
    DIAMONDS_7 = auto()
    DIAMONDS_8 = auto()
    DIAMONDS_9 = auto()
    DIAMONDS_10 = auto()
    DIAMONDS_JACK = auto()
    DIAMONDS_QUEEN = auto()
    DIAMONDS_KING = auto()
    DIAMONDS_ACE = auto()
    HEARTS_2 = auto()
    HEARTS_3 = auto()
    HEARTS_4 = auto()
    HEARTS_5 = auto()
    HEARTS_6 = auto()
    HEARTS_7 = auto()
    HEARTS_8 = auto()
    HEARTS_9 = auto()
    HEARTS_10 = auto()
    HEARTS_JACK = auto()
    HEARTS_QUEEN = auto()
    HEARTS_KING = auto()
    HEARTS_ACE = auto()
    SPADES_2 = auto()
    SPADES_3 = auto()
    SPADES_4 = auto()
    SPADES_5 = auto()
    SPADES_6 = auto()
    SPADES_7 = auto()
    SPADES_8 = auto()
    SPADES_9 = auto()
    SPADES_10 = auto()
    SPADES_JACK = auto()
    SPADES_QUEEN = auto()
    SPADES_KING = auto()
    SPADES_ACE = auto()


class Deck:
    """
    Represents the state of a deck of cards.
    """

    _random: random.Random
    _cards: list[Card]

    def __init__(self, random_seed: RandomSeed = None):
        """
        Args:
            random_seed: The seed value for the pseudo-random number generator that
            shuffles the deck of cards
        """
        self._random = random.Random(random_seed)
        self._cards = [
            Card.CLUBS_2,
            Card.CLUBS_3,
            Card.CLUBS_4,
            Card.CLUBS_5,
            Card.CLUBS_6,
            Card.CLUBS_7,
            Card.CLUBS_8,
            Card.CLUBS_9,
            Card.CLUBS_10,
            Card.CLUBS_JACK,
            Card.CLUBS_QUEEN,
            Card.CLUBS_KING,
            Card.CLUBS_ACE,
            Card.DIAMONDS_2,
            Card.DIAMONDS_3,
            Card.DIAMONDS_4,
            Card.DIAMONDS_5,
            Card.DIAMONDS_6,
            Card.DIAMONDS_7,
            Card.DIAMONDS_8,
            Card.DIAMONDS_9,
            Card.DIAMONDS_10,
            Card.DIAMONDS_JACK,
            Card.DIAMONDS_QUEEN,
            Card.DIAMONDS_KING,
            Card.DIAMONDS_ACE,
            Card.HEARTS_2,
            Card.HEARTS_3,
            Card.HEARTS_4,
            Card.HEARTS_5,
            Card.HEARTS_6,
            Card.HEARTS_7,
            Card.HEARTS_8,
            Card.HEARTS_9,
            Card.HEARTS_10,
            Card.HEARTS_JACK,
            Card.HEARTS_QUEEN,
            Card.HEARTS_KING,
            Card.HEARTS_ACE,
            Card.SPADES_2,
            Card.SPADES_3,
            Card.SPADES_4,
            Card.SPADES_5,
            Card.SPADES_6,
            Card.SPADES_7,
            Card.SPADES_8,
            Card.SPADES_9,
            Card.SPADES_10,
            Card.SPADES_JACK,
            Card.SPADES_QUEEN,
            Card.SPADES_KING,
            Card.SPADES_ACE,
        ]

    def shuffle(self) -> None:
        """
        Shuffles the cards in the deck.
        """
        self._random.shuffle(self._cards)

    def deal_card(self) -> Card:
        """
        Removes the top deal_card from the deck and returns it.
        """
        return self._cards.pop()


@dataclass
class Player:
    """
    `Player` represents the state of a player in a `Game`.
    """

    id: PlayerID
    stack_size: NumChips
    hole_cards: Tuple[Card, Card] | None = None
    bet_size: NumChips | None = None
    is_all_in: bool = False
    has_folded: bool = False


Pot = NewType("Pot", dict[PlayerID, NumChips])


@unique
class Round(Enum):
    """
    `Round` is the betting round in a `Game`.
    """

    PREFLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()


class Step:
    """
    `Step` represents a step in a `Game`.
    """


@dataclass(frozen=True)
class StartNewHand(Step):
    """
    `StartNewHand` is a step in a `Game` that starts a new hand.
    """


@dataclass(frozen=True)
class PostLittleBlind(Step):
    """
    `PostLittleBlind` is a step in a `Game` where the player in the little blind
    position must bet the little blind amount.
    """

    player_id: PlayerID


@dataclass(frozen=True)
class PostBigBlind(Step):
    """
    `PostBigBlind` is a step in a `Game` where the player in the big blind position
    must bet the big blind amount.
    """

    player_id: PlayerID


@dataclass(frozen=True)
class PlayerAction(Step):
    """
    `PlayerAction` is a step in a `Game` where a player must decide to check, call,
    raise, or fold.
    """

    player_id: PlayerID


@dataclass
class Game:
    """
    `Game` represents the state of a game of Texas Hold'em poker.
    """

    big_blind: NumChips
    little_blind: NumChips
    players: list[Player]
    button_position: int = 0
    round: Round | None = None
    last_raise_player_id: PlayerID | None = None
    last_raise_num_chips: NumChips | None = None
    pots: list[Pot] | None = None
    flop_cards: Tuple[Card, Card, Card] | None = None
    turn_card: Card | None = None
    river_card: Card | None = None

    def next_step(self) -> Step | None:
        if len(self.players) < 2:
            return None

        if self.round is None:
            return StartNewHand()

        if self.round == Round.PREFLOP:
            little_blind_position = (self.button_position + 1) % len(self.players)
            little_blind_player = self.players[little_blind_position]
            if little_blind_player.bet_size is None:
                return PostLittleBlind(little_blind_player.id)

            big_blind_position = (little_blind_position + 1) % len(self.players)
            big_blind_player = self.players[big_blind_position]
            if big_blind_player.bet_size is None:
                return PostBigBlind(big_blind_player.id)


@dataclass
class Room:
    """
    `Room` represents a room for playing games of poker.
    """

    id: RoomID
    players: list[Player]

    def __init__(self) -> None:
        self.id = RoomID(uuid.uuid4())

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the `Room`.
        """
        self.players.append(player)
