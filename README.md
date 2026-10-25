# 2048

A Python version of the 2048 puzzle game. The project includes a graphical interface built with Tkinter and a terminal version. Move the tiles on a 4 × 4 board, merge matching values, and try to reach 2048.

## Features

- Play in a Tkinter graphical window or in the terminal.
- Move tiles with the arrow keys or W/A/S/D in the graphical game.
- Merge equal tiles and earn points for each merge.
- Undo the last successful move and restart the board.
- View the rules from the game with the H key.
- Keep a saved game and high score between sessions.
- Detect when 2048 is reached and when no moves remain.

## Requirements

- Python 3
- Tkinter support for the graphical version. Tkinter is part of Python's standard library, but some Python installations package it separately.

The project uses no third-party Python packages, so `pip install` is not required. To check that Tkinter is available, run:

```bash
python3 -m tkinter
```

This opens a small sample window. Close it before launching the game. If the command reports that `tkinter` is unavailable, install Tk support for your Python installation.

## Run the graphical game

Open Terminal, change to the folder containing this project, and run:

```bash
python3 main.py
```

`main.py` is the default launcher and opens the graphical game in `gui.py`. You can also launch the graphical game directly with `python3 gui.py`.

## Run the terminal game

From the project folder, run:

```bash
python3 -c 'import main; main.main()'
```

The terminal version asks whether to continue an existing save or start a new game. Its controls are entered by typing a key and pressing Return.

## Controls

| Key | Action |
| --- | --- |
| `W` / `↑` | Move up |
| `A` / `←` | Move left |
| `S` / `↓` | Move down |
| `D` / `→` | Move right |
| `U` | Undo the last successful move |
| `R` | Start a new game and clear the saved board |
| `H` | Show the rules |
| `Q` | Open the save and next-action choices |

After a valid move, a new 2 or 4 tile is added. The game announces when you reach 2048, and you can keep playing. The game ends when the board is full and no matching neighboring tiles can merge.

In the graphical version, `Q` asks whether to save before showing choices to start a new game, continue playing, or exit. The window's close button opens the same choices. If a saved game exists on startup, choose **Yes** to continue it or **No** to start a new game. Starting a new game clears the saved board but preserves the high score.

## Saving

The game creates these files in the project folder:

- `2048.save.txt` stores the board, current score, and high score.
- `2048.highscore.txt` stores the best score separately so restarting does not erase it.

The graphical game saves when you choose to save on exit and when the game ends. It saves a new high score as soon as you beat the previous record. These files are created by the game; they are not dependencies.

## Tests

Run the game-logic tests from the project folder with:

```bash
python3 -m unittest discover -s tests -v
```

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Default launcher and terminal game logic |
| `gui.py` | Tkinter graphical interface |
| `board.py` | Creates the board and adds random tiles |
| `game_logic.py` | Handles moves, merges, score, win, and game-over checks |
| `file_manager.py` | Loads and saves game data and high scores |
| `tests/test_game_logic.py` | Tests core game logic |
| `gui2.py` | Older alternate GUI copy; not used by the default launcher |
