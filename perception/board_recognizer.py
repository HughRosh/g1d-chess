#!/usr/bin/env python3

"""
Board recognizer interface.

All chessboard perception backends should return a FEN string.
"""

class BoardRecognizer:
    def recognize(self, frame):
        raise NotImplementedError
