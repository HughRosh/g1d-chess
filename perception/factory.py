#!/usr/bin/env python3

def make_board_recognizer(backend="mock"):
    if backend == "mock":
        from perception.mock_board_recognizer import MockBoardRecognizer
        return MockBoardRecognizer()

    if backend == "chesscog":
        from perception.chesscog_backend import ChesscogBackend
        return ChesscogBackend()

    raise ValueError(f"Unknown board recognizer backend: {backend}")
