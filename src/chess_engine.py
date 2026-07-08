import chess

def choose_move(board):
    """
    Temporary move chooser.
    Later this will call Stockfish.
    """
    move = chess.Move.from_uci("e2e4")

    if move in board.legal_moves:
        return move

    return next(iter(board.legal_moves))
