#!/usr/bin/env python3

from perception.board_recognizer import BoardRecognizer


class MockBoardRecognizer(BoardRecognizer):
    def recognize(self, frame=None):
        # Standard starting chess position
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
