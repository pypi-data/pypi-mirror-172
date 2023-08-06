from bluffai import (
    Game,
    NumChips,
    Player,
    PlayerAgentAddress,
    PlayerID,
    Room,
    StartNewHand,
)


def test_game_next_step_none():
    game = Game(
        big_blind=2,
        little_blind=1,
        players=[],
    )
    assert game.next_step() is None

    game = Game(
        big_blind=2,
        little_blind=1,
        players=[
            Player(
                id="player-0",
                stack_size=100,
            ),
        ],
    )
    assert game.next_step() is None


def test_game_next_step_start_new_hand():
    game = Game(
        big_blind=2,
        little_blind=1,
        players=[
            Player(
                id="player-0",
                stack_size=100,
            ),
            Player(
                id="player-1",
                stack_size=100,
            ),
            Player(
                id="player-2",
                stack_size=100,
            ),
        ],
    )
    assert game.next_step() == StartNewHand()
