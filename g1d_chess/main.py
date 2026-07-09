import argparse

from g1d_chess.envs.chess_manipulation_env import ChessManipulationEnv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--move", default="e2e4")
    parser.add_argument("--arm", default="right")
    args = parser.parse_args()

    env = ChessManipulationEnv(arm=args.arm)
    print(env.observe())
    env.execute_move(args.move)


if __name__ == "__main__":
    main()
