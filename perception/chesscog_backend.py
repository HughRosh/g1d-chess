#!/usr/bin/env python3

from perception.board_recognizer import BoardRecognizer


class ChesscogBackend(BoardRecognizer):
    def __init__(self):
        raise NotImplementedError(
            "Chesscog backend placeholder. "
            "Install and wrap Chesscog here later."
        )

    def recognize(self, frame):
        raise NotImplementedError
