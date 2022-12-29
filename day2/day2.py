# Advent of Code: Day 2
__author__ = "Matteo Golin"

# Imports

# Constants
INPUT_FILE = "./input.txt"
SYMBOL_MAP = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}
OUTCOME_MAP = {
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}
SCORE_MAP = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
    "win": 6,
    "draw": 3,
    "lose": 0,
}
WIN_MAP = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock"
}


# Main
def game_score(opponent_move: str, player_move: str) -> int:

    """Returns the player score for the round."""

    symbol_score = SCORE_MAP[player_move]  # Account for chosen shape

    # Draw
    if opponent_move == player_move:
        return symbol_score + SCORE_MAP["draw"]

    # Win/Loss
    if symbol_score % 3 == SCORE_MAP[opponent_move] - 1:
        return symbol_score + SCORE_MAP["lose"]
    else:
        return symbol_score + SCORE_MAP["win"]


def score_from_outcome(opponent_move: str, outcome: str) -> int:

    """Calculates the score from the required player move to satisfy the outcome."""

    if outcome == "draw":
        player_move: str = opponent_move
    elif outcome == "win":
        player_move: str = WIN_MAP[opponent_move]
    else:  # Lose
        player_move: str = WIN_MAP[opponent_move]
        player_move: str = WIN_MAP[player_move]

    return SCORE_MAP[player_move] + SCORE_MAP[outcome]


def main():

    # Part 1
    # Calculate player score assuming second column indicates which move should be played
    player_score: int = 0
    with open(INPUT_FILE, 'r') as file:

        # Each line represents a round
        for line in file:
            opponent, player = line.strip().split(" ")  # Unpack moves

            # Map moves
            opponent: str = SYMBOL_MAP[opponent]
            player: str = SYMBOL_MAP[player]

            player_score += game_score(opponent, player)

    print(f"The player's final score using the assumed strategy is {player_score} points.")

    # Part 2
    # Calculate the player score if the strategy is implemented where the second column indicates the
    # game outcome
    player_strategy_score: int = 0
    with open(INPUT_FILE, 'r') as file:

        # Each line represents a round
        for line in file:
            opponent, outcome = line.strip().split(" ")  # Unpack moves

            # Map moves
            opponent: str = SYMBOL_MAP[opponent]
            outcome: str = OUTCOME_MAP[outcome]

            player_strategy_score += score_from_outcome(opponent, outcome)

    print(f"The player's final score using the elf strategy is {player_strategy_score} points.")


if __name__ == '__main__':
    main()
