import board
import game_logic
import file_manager


def show_rules():
    print("\n              # RULES #               ")
    print("\nW → For moving grid in upward direction.")
    print("A → For moving grid in left direction.")
    print("S → For moving grid in downward direction.")
    print("D → For moving grid in right direction.")
    print("U → To undo the last move.")
    print("Q → To quit the game.")
    print("R → To reset the game.")
    print("H → To show these rules.\n")


def start_new_game(clear_saved_game=True):
    # Clear the old saved board when the user starts a replacement game.
    if clear_saved_game:
        file_manager.reset_game()
    board.a.rows = [[0] * 4 for _ in range(4)]
    board.a.add_random_tile()
    board.a.add_random_tile()
    game_logic.score = 0


def show_score(high_score):
    print("\n     Your Score is :", game_logic.score)
    print("\n     High score is :", high_score)


def finish_move(high_score, win_announced):
    # Add a new tile after a move that changed the board.
    board.a.add_random_tile()
    board.a.display()

    # Keep the highest score in its own file.
    if game_logic.score > high_score:
        high_score = game_logic.score
        file_manager.save_high_score(high_score)

    # Check for a win after every valid move, not only at game over.
    if not win_announced and game_logic.Game_win(board.a.rows):
        print("\n    # CONGRATULATIONS — YOU REACHED 2048! #")
        win_announced = True

    show_score(high_score)
    return high_score, win_announced


def main():
    # Create the board here so importing board.py does not start a game.
    board.a = board.Board()

    print("\n          WELCOME TO 2048")
    print("GOAL : To achieve 2048 in one of the grid.\n")
    show_rules()

    # Load the previous game if a valid save file is available.
    data = file_manager.load_game()
    high_score = file_manager.load_high_score()
    if data is not None:
        high_score = max(high_score, data["high score"])
        # Keep older save files' high scores when starting a new game.
        file_manager.save_high_score(high_score)

    game_logic.score = 0
    win_announced = False
    previous_board = None
    previous_score = 0
    previous_win_announced = False
    can_undo = False

    if data is None:
        start_new_game()
        previous_board = None
        can_undo = False
    else:
        choice = input(
            "What do you want to do?\n"
            "Continue game (C)\n"
            "New game      (N)\n"
        ).strip().lower()

        if choice == "c":
            print("Game continued successfully!\n")
            board.a.rows = data["board"]
            game_logic.score = data["score"]
        else:
            start_new_game()
            previous_board = None
            can_undo = False

    board.a.display()
    show_score(high_score)

    if game_logic.Game_win(board.a.rows):
        print("\nYou have already reached 2048. You can keep playing.\n")
        win_announced = True

    # Main game loop
    while True:
        if game_logic.Game_over(board.a.rows):
            high_score = max(high_score, game_logic.score)
            file_manager.save_game(board.a.rows, game_logic.score, high_score)

            if game_logic.Game_win(board.a.rows):
                if not win_announced:
                    print("\n    # CONGRATULATIONS #")
            else:
                print("\n    # NO MORE MOVES — GAME OVER #")

            choice = input(
                "\nDo you want to start a new game?\n"
                "YES (Y)\nUNDO LAST MOVE (U)\nNO  (N)\n"
            ).strip().lower()

            if choice == "y":
                start_new_game()
                previous_board = None
                can_undo = False
                win_announced = False
                board.a.display()
                show_score(high_score)
                continue

            elif choice == "u":
                if can_undo:
                    board.a.rows = previous_board
                    game_logic.score = previous_score
                    win_announced = previous_win_announced
                    can_undo = False

                    # Replace the saved game-over board with the restored board.
                    file_manager.save_game(board.a.rows, game_logic.score, high_score)
                    board.a.display()
                    show_score(high_score)
                else:
                    print("\nThere is no move to undo.")
                continue

            break

        move = input("\nEnter your move (W/A/S/D, U to undo, H for help, Q to quit): ").strip().lower()

        # Move Up
        if move == "w":
            old_board = [row[:] for row in board.a.rows]
            old_score = game_logic.score
            old_win_announced = win_announced

            board.a.rows = game_logic.move_up(board.a.rows)
            if game_logic.check:
                previous_board = old_board
                previous_score = old_score
                previous_win_announced = old_win_announced
                can_undo = True
                high_score, win_announced = finish_move(high_score, win_announced)
            else:
                print("\nYou can't move upward.")

        # Move Down
        elif move == "s":
            old_board = [row[:] for row in board.a.rows]
            old_score = game_logic.score
            old_win_announced = win_announced

            board.a.rows = game_logic.move_down(board.a.rows)
            if game_logic.check:
                previous_board = old_board
                previous_score = old_score
                previous_win_announced = old_win_announced
                can_undo = True
                high_score, win_announced = finish_move(high_score, win_announced)
            else:
                print("\nYou can't move downward.")

        # Move Left
        elif move == "a":
            old_board = [row[:] for row in board.a.rows]
            old_score = game_logic.score
            old_win_announced = win_announced

            board.a.rows = game_logic.move_left(board.a.rows)
            if game_logic.check:
                previous_board = old_board
                previous_score = old_score
                previous_win_announced = old_win_announced
                can_undo = True
                high_score, win_announced = finish_move(high_score, win_announced)
            else:
                print("\nYou can't move left.")

        # Move Right
        elif move == "d":
            old_board = [row[:] for row in board.a.rows]
            old_score = game_logic.score
            old_win_announced = win_announced

            board.a.rows = game_logic.move_right(board.a.rows)
            if game_logic.check:
                previous_board = old_board
                previous_score = old_score
                previous_win_announced = old_win_announced
                can_undo = True
                high_score, win_announced = finish_move(high_score, win_announced)
            else:
                print("\nYou can't move right.")

        # Undo the last successful move
        elif move == "u":
            if can_undo:
                board.a.rows = previous_board
                game_logic.score = previous_score
                win_announced = previous_win_announced
                can_undo = False

                print("\nLast move undone.")
                board.a.display()
                show_score(high_score)
            else:
                print("\nThere is no move to undo.")

        # Quit Game
        elif move == "q":
            choice = input("Do you want to save this game? YES (Y) / NO (N): ").strip().lower()
            if choice == "y":
                file_manager.save_game(board.a.rows, game_logic.score, high_score)

            choice = input(
                "New Game (1)\nContinue this game (2)\nExit (any other key)\n"
            ).strip().lower()

            if choice == "1":
                # Keep a saved game when starting a second game after Q.
                start_new_game(clear_saved_game=False)
                previous_board = None
                can_undo = False
                win_announced = False
                board.a.display()
                show_score(high_score)
            elif choice == "2":
                print("Continuing the current game.\n")
            else:
                break

        # Reset Game
        elif move == "r":
            start_new_game()
            previous_board = None
            can_undo = False
            win_announced = False
            board.a.display()
            show_score(high_score)

        # Help Menu
        elif move == "h":
            show_rules()

        # Invalid input
        else:
            print("\nINVALID INPUT. For help, press H.\n")


if __name__ == "__main__":
    import gui
