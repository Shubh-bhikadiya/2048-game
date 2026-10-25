import json
import os

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(PROJECT_FOLDER, "2048.save.txt")
HIGH_SCORE_FILE = os.path.join(PROJECT_FOLDER, "2048.highscore.txt")


def load_high_score():
    """Load the best score saved in 2048.highscore.txt."""
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            high_score = int(file.read().strip())

        if high_score < 0:
            return 0
        return high_score
    except FileNotFoundError:
        return 0
    except (ValueError, OSError, UnicodeError) as error:
        print(f"Could not load the high score: {error}")
        return 0


def save_high_score(high_score):
    """Save the best score separately so Reset can keep it."""
    try:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(high_score))
    except OSError as error:
        print(f"Error saving high score: {error}")


def save_game(board, score, high_score):
    """Save the current board and score to 2048.save.txt."""
    data = {
        "version": 1,
        "board": board,
        "score": score,
        "high_score": high_score,
    }

    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(data, file)
        save_high_score(high_score)
        print("\n   Game saved successfully!\n")
    except (OSError, TypeError) as error:
        print(f"Error saving game: {error}")


def load_game():
    """Load a valid saved board, or return None when there is no usable save."""
    try:
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, OSError, UnicodeError) as error:
        print(f"Could not load the saved game: {error}")
        return None

    if not isinstance(data, dict):
        print("The saved game is invalid. Starting a new game.")
        return None

    saved_board = data.get("board")
    score = data.get("score")

    board_is_valid = (
        isinstance(saved_board, list)
        and len(saved_board) == 4
        and all(isinstance(row, list) and len(row) == 4 for row in saved_board)
        and all(
            type(value) is int and value >= 0
            for row in saved_board
            for value in row
        )
    )

    if not board_is_valid or type(score) is not int or score < 0:
        print("The saved game is incomplete or invalid. Starting a new game.")
        return None

    saved_high_score = data.get("high_score", data.get("high score", 0))
    if type(saved_high_score) is not int or saved_high_score < 0:
        saved_high_score = 0

    high_score = max(saved_high_score, load_high_score())

    return {
        "board": saved_board,
        "score": score,
        "high score": high_score,
    }


def reset_game():
    """Delete the saved board while keeping the separate high score."""
    try:
        os.remove(SAVE_FILE)
        print("\nSaved game cleared. High score kept.\n")
    except FileNotFoundError:
        print("\nThere is no saved game to clear.\n")
    except OSError as error:
        print(f"Error clearing the saved game: {error}")
