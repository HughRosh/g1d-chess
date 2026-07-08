import chess
import chess.engine

def choose_move(board, stockfish_path=None, time_limit=0.1):
    """
    Choose a legal chess move.

    If stockfish_path is provided, use Stockfish.
    Otherwise, use a simple fallback move.
    """
    if stockfish_path:
        try:
            with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
                result = engine.play(board, chess.engine.Limit(time=time_limit))
                return result.move
        except Exception as e:
            print(f"Stockfish unavailable, using fallback move: {e}")

    preferred = chess.Move.from_uci("e2e4")
    if preferred in board.legal_moves:
        return preferred

    return next(iter(board.legal_moves))
