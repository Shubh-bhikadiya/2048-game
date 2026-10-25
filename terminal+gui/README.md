# 2048 — Python Puzzle Game

A Python implementation of the classic 2048 puzzle. Play on a 4 × 4 board, slide numbered tiles, merge matching values, and try to create a tile worth 2048. The project provides a Tkinter desktop interface, a terminal version, and a browser version in `docs/` that can be published with GitHub Pages.

## Features

- Graphical game window with arrow-key and W/A/S/D controls.
- Terminal version with text-based board display.
- Browser version built with HTML, CSS, and JavaScript.
- Tile movement, merging, score updates, and random tile placement.
- One-move undo and game restart.
- Win and game-over detection. Reaching 2048 does not stop play.
- A saved game that can be continued later, plus a high score that persists across restarts.
- Help instructions in both versions.

## Requirements

- Python 3.
- Tkinter to run the graphical version. Tkinter is part of Python's standard library, although some Python distributions install its support separately.

The project uses no third-party Python packages, so you do not need to install packages with `pip` or create a virtual environment. There is no `requirements.txt` file.

To check your Python version and confirm that Tkinter is available, run:

```bash
python3 --version
python3 -m tkinter
```

The Tkinter command opens a small sample window. Close it before starting the game. If it reports that Tkinter is missing, install the Tk support that matches your Python distribution and version.

## Run the graphical game

Open Terminal and change to the folder containing `main.py`. Replace the example path below if you saved the project somewhere else:

```bash
cd /path/to/2048
python3 main.py
```

`main.py` is the default launcher. It opens the current graphical game from `gui.py`. You can also start the GUI directly with:

```bash
python3 gui.py
```

## Preview the browser game

From the project folder, start Python's built-in web server:

```bash
python3 -m http.server 8000 --directory docs
```

Open [http://localhost:8000](http://localhost:8000) in your browser. This serves the static files in `docs/`; it does not start the Tkinter game. Keep Terminal open while playing locally, and press `Control+C` in Terminal to stop the server.

The browser version saves its current game and best score in that browser's local storage. This data stays in that browser and is not shared with other visitors.

## Publish with GitHub Pages

Upload the project to a GitHub repository, then open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select the `main` branch and the `/docs` folder, and save. GitHub Pages uses `docs/index.html` as the site's entry page. The website link appears in the Pages settings.

## Run the terminal game

From the same project folder, run:

```bash
python3 -c 'import main; main.main()'
```

The terminal version first shows the rules. If a valid saved game exists, it asks whether you want to continue it or start a new game. Enter a control key and press Return to make a selection or move.

## How to play

The board begins with two tiles. Use a direction key to slide every tile as far as possible in that direction. When two tiles with the same value meet, they merge into one tile with their values added together. Each successful move adds a new tile: usually a 2, and sometimes a 4. A move that does not change the board does not add a tile.

The score increases by the value of each merged tile. The goal is to create a 2048 tile. After reaching 2048, you can continue playing. The game is over when the board is full and no neighboring tiles can merge.

### Graphical controls

| Key | Action |
| --- | --- |
| `W` or `↑` | Move up |
| `A` or `←` | Move left |
| `S` or `↓` | Move down |
| `D` or `→` | Move right |
| `U` | Undo the last successful move |
| `R` | Start a new game and clear the saved board |
| `H` | Open the help window |
| `Q` | Open the save and next-action choices |

The window's close button opens the same choices as `Q`. When the game is over, the board is saved automatically. You can press `U` to undo the move that ended the game or `R` to start over.

### Terminal controls

Type one of these keys and press Return:

| Key | Action |
| --- | --- |
| `W` | Move up |
| `A` | Move left |
| `S` | Move down |
| `D` | Move right |
| `U` | Undo the last successful move |
| `R` | Start a new game and clear the saved board |
| `H` | Print the rules |
| `Q` | Open the save and next-action choices |

## Saving and continuing

The game stores its data in two files beside `file_manager.py`:

- `2048.save.txt` stores the board, current score, and high score. The data is written as JSON even though the file ends in `.txt`.
- `2048.highscore.txt` stores the best score separately so that starting a new game does not erase it.

When the graphical game opens and finds a saved game, choose **Yes** to continue or **No** to start a new game. Choosing **No** clears the previous saved board but keeps the high score.

When you press `Q` or close the window, the GUI first asks whether to save the current game. It then asks what to do next:

- **Yes** starts a new game and keeps the saved game file.
- **No** returns to the current game.
- **Cancel** exits the program.

The GUI does not save after every move. Choose **Yes** in the save prompt to keep your latest board and score. The game also saves the board when it ends, and saves a new high score as soon as you beat the previous record. Pressing `R` clears the saved board but keeps the high score.

The terminal version has equivalent choices: at startup, enter `C` to continue or `N` to start a new game; at `Q`, enter `Y` or `N` to save, then choose `1` for a new game, `2` to continue, or another key to exit.

## Run the tests

The current test suite covers the core game logic. From the project folder, run:

```bash
python3 -m unittest discover -s tests -v
```

## Project structure

| File or folder | Purpose |
| --- | --- |
| `main.py` | Default GUI launcher and terminal game implementation |
| `gui.py` | Tkinter window, board display, keyboard controls, and dialogs |
| `board.py` | Creates the 4 × 4 board and adds random tiles |
| `game_logic.py` | Handles movement, merges, score, win detection, and game-over detection |
| `file_manager.py` | Reads and writes saved games and high scores |
| `docs/index.html` | Browser game's page and board structure |
| `docs/style.css` | Browser game's layout, colors, and responsive styling |
| `docs/game.js` | Browser rules, controls, scoring, and local storage |
| `tests/test_game_logic.py` | Tests for the core game rules |
| `gui2.py` | Older alternate GUI copy; it is not used by the default launcher |
| `2048.save.txt` | Generated saved-game data, created when the game saves |
| `2048.highscore.txt` | Generated high-score data, created when a high score is saved |
