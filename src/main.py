from board_detector import detect_board_state
from chess_engine import choose_move
from board_geometry import move_to_pick_place
from arm_planner import make_pick_place_motion
from robot_controller import execute_motion
from utils import load_config

def main():
    config = load_config("configs/chess.yaml")

    board = detect_board_state()

    engine_cfg = config.get("engine", {})
    move = choose_move(
        board,
        stockfish_path=engine_cfg.get("stockfish_path"),
        time_limit=engine_cfg.get("time_limit_s", 0.1),
    )

    board.push(move)

    plan = move_to_pick_place(move.uci(), config)
    motion = make_pick_place_motion(plan, config)

    print("G1-D Chess")
    print(f"Chosen move: {move.uci()}")
    print(f"Board FEN after move: {board.fen()}")

    execute_motion(motion, dry_run=True)

if __name__ == "__main__":
    main()
