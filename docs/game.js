"use strict";

const GRID_SIZE = 4;
const SAVE_KEY = "2048-web-save-v1";
const BEST_SCORE_KEY = "2048-web-best-score-v1";

const boardElement = document.querySelector("#board");
const scoreElement = document.querySelector("#score");
const bestScoreElement = document.querySelector("#best-score");
const messageElement = document.querySelector("#game-message");
const undoButton = document.querySelector("#undo-button");
const newGameButton = document.querySelector("#new-game-button");

let board = makeEmptyBoard();
let score = 0;
let bestScore = readBestScore();
let previousMove = null;
let hasWon = false;

function makeEmptyBoard() {
  return Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));
}

function copyBoard(currentBoard) {
  return currentBoard.map((row) => row.slice());
}

function readBestScore() {
  try {
    const storedScore = Number(localStorage.getItem(BEST_SCORE_KEY));
    return Number.isFinite(storedScore) && storedScore >= 0 ? storedScore : 0;
  } catch (error) {
    return 0;
  }
}

function isValidBoard(candidate) {
  return Array.isArray(candidate)
    && candidate.length === GRID_SIZE
    && candidate.every((row) => Array.isArray(row)
      && row.length === GRID_SIZE
      && row.every((value) => Number.isInteger(value) && value >= 0));
}

function readSavedGame() {
  try {
    const savedText = localStorage.getItem(SAVE_KEY);
    if (!savedText) {
      return null;
    }

    const savedGame = JSON.parse(savedText);
    if (!isValidBoard(savedGame.board)
      || !Number.isInteger(savedGame.score)
      || savedGame.score < 0) {
      return null;
    }

    return savedGame;
  } catch (error) {
    return null;
  }
}

function saveGame() {
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify({
      board,
      score,
      hasWon,
    }));
  } catch (error) {
    showMessage("Your browser could not save this game.");
  }
}

function saveBestScore() {
  try {
    localStorage.setItem(BEST_SCORE_KEY, String(bestScore));
  } catch (error) {
    showMessage("Your browser could not save the best score.");
  }
}

function showMessage(message) {
  messageElement.textContent = message;
}

function addRandomTile() {
  const emptyCells = [];

  for (let row = 0; row < GRID_SIZE; row += 1) {
    for (let column = 0; column < GRID_SIZE; column += 1) {
      if (board[row][column] === 0) {
        emptyCells.push({ row, column });
      }
    }
  }

  if (emptyCells.length === 0) {
    return;
  }

  const location = emptyCells[Math.floor(Math.random() * emptyCells.length)];
  board[location.row][location.column] = Math.random() < 0.8 ? 2 : 4;
}

function slideLine(line) {
  const packedLine = line.filter((value) => value !== 0);
  const mergedLine = [];
  let scoreGained = 0;

  for (let index = 0; index < packedLine.length; index += 1) {
    if (packedLine[index] === packedLine[index + 1]) {
      const mergedValue = packedLine[index] * 2;
      mergedLine.push(mergedValue);
      scoreGained += mergedValue;
      index += 1;
    } else {
      mergedLine.push(packedLine[index]);
    }
  }

  while (mergedLine.length < GRID_SIZE) {
    mergedLine.push(0);
  }

  return { line: mergedLine, scoreGained };
}

function transpose(currentBoard) {
  return currentBoard[0].map((value, column) =>
    currentBoard.map((row) => row[column]));
}

function slideRows(rows, direction) {
  let scoreGained = 0;
  const nextRows = rows.map((row) => {
    const lineToSlide = direction === "right" ? row.slice().reverse() : row;
    const result = slideLine(lineToSlide);
    scoreGained += result.scoreGained;
    return direction === "right" ? result.line.reverse() : result.line;
  });

  return { board: nextRows, scoreGained };
}

function boardsAreEqual(firstBoard, secondBoard) {
  return firstBoard.every((row, rowIndex) =>
    row.every((value, columnIndex) => value === secondBoard[rowIndex][columnIndex]));
}

function boardHas2048(currentBoard) {
  return currentBoard.some((row) => row.some((value) => value >= 2048));
}

function isGameOver() {
  for (let row = 0; row < GRID_SIZE; row += 1) {
    for (let column = 0; column < GRID_SIZE; column += 1) {
      const value = board[row][column];

      if (value === 0) {
        return false;
      }

      if (column + 1 < GRID_SIZE && value === board[row][column + 1]) {
        return false;
      }

      if (row + 1 < GRID_SIZE && value === board[row + 1][column]) {
        return false;
      }
    }
  }

  return true;
}

function renderBoard() {
  boardElement.replaceChildren();

  for (let row = 0; row < GRID_SIZE; row += 1) {
    for (let column = 0; column < GRID_SIZE; column += 1) {
      const value = board[row][column];
      const tile = document.createElement("div");
      tile.classList.add("tile");
      tile.classList.add(value === 0 ? "tile-empty" : `tile-${value}`);
      if (value >= 2048) {
        tile.classList.add("tile-large");
      }
      tile.setAttribute("role", "gridcell");
      tile.setAttribute("aria-label", value === 0 ? "Empty" : String(value));
      tile.textContent = value === 0 ? "" : String(value);
      boardElement.appendChild(tile);
    }
  }

  scoreElement.textContent = String(score);
  bestScoreElement.textContent = String(bestScore);
  undoButton.disabled = previousMove === null;
}

function startNewGame(askFirst = true) {
  if (askFirst && !window.confirm("Start a new game? Your current game will be replaced.")) {
    return;
  }

  board = makeEmptyBoard();
  score = 0;
  previousMove = null;
  hasWon = false;
  addRandomTile();
  addRandomTile();
  showMessage("Use the arrow keys or W, A, S, D to move.");
  saveGame();
  renderBoard();
}

function move(direction) {
  if (isGameOver()) {
    showMessage("No moves remain. Start a new game or undo the last move.");
    return;
  }

  const oldBoard = copyBoard(board);
  const oldScore = score;
  const oldHasWon = hasWon;
  const isVertical = direction === "up" || direction === "down";
  const rowsToSlide = isVertical ? transpose(board) : copyBoard(board);
  const lineDirection = direction === "up" ? "left" : direction === "down" ? "right" : direction;
  const slid = slideRows(rowsToSlide, lineDirection);
  const nextBoard = isVertical ? transpose(slid.board) : slid.board;

  if (boardsAreEqual(board, nextBoard)) {
    showMessage("That move does not change the board.");
    return;
  }

  previousMove = {
    board: oldBoard,
    score: oldScore,
    hasWon: oldHasWon,
  };
  board = nextBoard;
  score += slid.scoreGained;
  addRandomTile();

  if (score > bestScore) {
    bestScore = score;
    saveBestScore();
  }

  const reached2048 = boardHas2048(board);
  const firstTimeWin = reached2048 && !hasWon;
  hasWon = hasWon || reached2048;

  if (isGameOver()) {
    showMessage(reached2048 ? "No moves remain. You reached 2048!" : "No moves remain. Start a new game or undo.");
  } else if (firstTimeWin) {
    showMessage("You reached 2048! Keep playing if you like.");
  } else {
    showMessage("Use the arrow keys or W, A, S, D to move.");
  }

  saveGame();
  renderBoard();
}

function undoMove() {
  if (previousMove === null) {
    showMessage("There is no move to undo.");
    return;
  }

  board = previousMove.board;
  score = previousMove.score;
  hasWon = previousMove.hasWon;
  previousMove = null;
  showMessage("Last move undone.");
  saveGame();
  renderBoard();
}

function initializeGame() {
  const savedGame = readSavedGame();

  if (savedGame) {
    board = savedGame.board;
    score = savedGame.score;
    hasWon = Boolean(savedGame.hasWon) || boardHas2048(board);
    bestScore = Math.max(bestScore, score);
    saveBestScore();
    showMessage("Your saved game was restored in this browser.");
  } else {
    startNewGame(false);
  }

  renderBoard();
}

document.addEventListener("keydown", (event) => {
  const key = event.key.toLowerCase();
  const directions = {
    arrowup: "up",
    w: "up",
    arrowleft: "left",
    a: "left",
    arrowdown: "down",
    s: "down",
    arrowright: "right",
    d: "right",
  };

  if (directions[key]) {
    event.preventDefault();
    move(directions[key]);
  } else if (key === "u") {
    undoMove();
  } else if (key === "r") {
    startNewGame();
  }
});

document.querySelectorAll("[data-direction]").forEach((button) => {
  button.addEventListener("click", () => move(button.dataset.direction));
});

undoButton.addEventListener("click", undoMove);
newGameButton.addEventListener("click", () => startNewGame());

initializeGame();
