#!/usr/bin/env python3

from pathlib import Path
import sys
import chess

sys.path.append(str(Path(__file__).resolve().parents[1]))

from perception.factory import make_board_recognizer


def main():
    recognizer = make_board_recognizer("mock")
    fen = recognizer.recognize()

    print("Recognized FEN:")
    print(fen)

    board = chess.Board(fen)
    print()
    print(board)


if __name__ == "__main__":
    main()
