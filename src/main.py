from board_detector import detect_board_state
from chess_engine import choose_move
from board_geometry import move_to_pick_place
from arm_planner import make_pick_place_motion
from robot_controller import execute_motion

def main():
    board = detect_board_state()
    move = choose_move(board)

    board.push(move)

    plan = move_to_pick_place(move.uci())
    motion = make_pick_place_motion(plan)

    print("G1-D Chess")
    print(f"Chosen move: {move.uci()}")
    print(f"Board FEN after move: {board.fen()}")

    execute_motion(motion, dry_run=True)

if __name__ == "__main__":
    main()
