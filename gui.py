import tkinter as tk
from tkinter import messagebox
import board
import file_manager
import game_logic

window = tk.Tk()
window.title("2048")
window.geometry("420x500")
window.resizable(False, False)

game_board = board.Board()
game_logic.score = 0
high_score = file_manager.load_high_score()
saved_game = file_manager.load_game()

if saved_game is not None:
    high_score = max(high_score, saved_game["high score"])
    file_manager.save_high_score(high_score)

    continue_game = messagebox.askyesno(
        "Saved game found",
        "Do you want to continue your saved game?\n\n"
        "Choose No to start a new game.",
        parent=window
    )

    if continue_game:
        game_board.rows = saved_game["board"]
        game_logic.score = saved_game["score"]
    else:
        file_manager.reset_game()
previous_board = None
previous_score = 0
can_undo = False

title_text = tk.Label(
    window,
    text="2048",
    font=("Arial", 32, "bold"),
    fg="#776e65"
)
title_text.pack(pady=5)

score_text = tk.Label(
    window,
    text="Score: 0",
    font=("Arial", 16, "bold"),
    fg="#776e65"
)
high_score_text = tk.Label(
    window,
    text="High score: " + str(high_score),
    font=("Arial", 16, "bold"),
    fg="#776e65"
)
high_score_text.pack()
score_text.pack(pady=5)
help_text = tk.Label(
    window,
    text="Move: W/A/S/D or arrows\nUndo: U    Restart: R    Help: H    Quit: Q",
    font=("Arial", 10),
    fg="#776e65"
)
help_text.pack(pady=2)

status_text = tk.Label(
    window,
    text="",
    font=("Arial", 12, "bold"),
    fg="#776e65"
)
status_text.pack(pady=2)
board_frame = tk.Frame(window, bg="#bbada0")
board_frame.pack(padx=15, pady=10)


def quit_game():
    global previous_board, previous_score, can_undo

    save_game = messagebox.askyesno(
        "Save game?",
        "Do you want to save this game before quitting?",
        parent=window
    )

    if save_game:
        file_manager.save_game(game_board.rows, game_logic.score, high_score)

    next_action = messagebox.askyesnocancel(
        "What next?",
        "Do you want to start a new game?\n\n"
        "Yes: Start a new game\n"
        "No: Continue this game\n"
        "Cancel: Exit",
        parent=window
    )

    if next_action is True:
        # Keep the saved game, like the terminal version's New Game choice.
        game_board.rows = [[0] * 4 for _ in range(4)]
        game_board.add_random_tile()
        game_board.add_random_tile()
        game_logic.score = 0
        previous_board = None
        previous_score = 0
        can_undo = False
        draw_board()
    elif next_action is None:
        window.destroy()


def update_status():
    if game_logic.Game_over(game_board.rows):
        if game_logic.Game_win(game_board.rows):
            status_text.config(text="Game over. You reached 2048!")
        else:
            status_text.config(text="Game over. Press R to restart.")
    elif game_logic.Game_win(game_board.rows):
        status_text.config(text="You reached 2048! Keep playing.")
    else:
        status_text.config(text="")

def draw_board():
    # Remove the old tiles before drawing the new board.
    for tile in board_frame.winfo_children():
        tile.destroy()

    score_text.config(text="Score: " + str(game_logic.score))
    high_score_text.config(text="High score: " + str(high_score))
    for row in range(4):
        for column in range(4):
            value = game_board.rows[row][column]

            if value == 0:
                tile_text = ""
                tile_color = "#cdc1b4"
            else:
                tile_text = str(value)
                tile_color = "#eee4da"

            tile = tk.Label(
                board_frame,
                text=tile_text,
                width=4,
                height=2,
                font=("Arial", 24, "bold"),
                bg=tile_color,
                fg="#776e65"
            )
            tile.grid(row=row, column=column, padx=5, pady=5)

    update_status()


def handle_key(event):
    global previous_board, previous_score, can_undo, high_score

    key = event.keysym.lower()

    if key == "q":
        quit_game()
        return

    if key == "r":
        file_manager.reset_game()
        game_board.rows = [[0] * 4 for _ in range(4)]
        game_board.add_random_tile()
        game_board.add_random_tile()
        game_logic.score = 0
        previous_board = None
        can_undo = False
        draw_board()
        return

    if key == "u":
        if can_undo:
            was_game_over = game_logic.Game_over(game_board.rows)
            game_board.rows = previous_board
            game_logic.score = previous_score
            can_undo = False
            if was_game_over:
                file_manager.save_game(game_board.rows, game_logic.score, high_score)
            draw_board()
        else:
            status_text.config(text="There is no move to undo.")
        return

    if key == "h":
        messagebox.showinfo(
            "How to play",
            "Use W/A/S/D or arrow keys to move tiles.\n"
            "Matching tiles combine and add to your score.\n"
            "Press U to undo one move.\n"
            "Press R to start a new game.\n"
            "Press Q to quit."
        )
        return

    if game_logic.Game_over(game_board.rows):
        return

    old_board = [row[:] for row in game_board.rows]
    old_score = game_logic.score

    if key == "w" or key == "up":
        game_board.rows = game_logic.move_up(game_board.rows)
    elif key == "s" or key == "down":
        game_board.rows = game_logic.move_down(game_board.rows)
    elif key == "a" or key == "left":
        game_board.rows = game_logic.move_left(game_board.rows)
    elif key == "d" or key == "right":
        game_board.rows = game_logic.move_right(game_board.rows)
    else:
        return

    if game_logic.check:
        if game_logic.score > high_score:
            high_score = game_logic.score
            file_manager.save_high_score(high_score)

        previous_board = old_board
        previous_score = old_score
        can_undo = True
        game_board.add_random_tile()
        if game_logic.Game_over(game_board.rows):
            file_manager.save_game(game_board.rows, game_logic.score, high_score)
        draw_board()
        


draw_board()
window.bind("<Key>", handle_key)
window.protocol("WM_DELETE_WINDOW", quit_game)
window.focus_set()

window.mainloop()
