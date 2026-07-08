from chess_engine import get_test_move
from board_geometry import move_to_pick_place
from arm_planner import make_pick_place_motion

def main():
    fen, move = get_test_move()
    plan = move_to_pick_place(move)
    motion = make_pick_place_motion(plan)

    print("G1-D Chess")
    print(f"Test move: {move}")
    print(f"Board FEN: {fen}")
    print("Motion plan:")

    for step in motion:
        print(step)

if __name__ == "__main__":
    main()
