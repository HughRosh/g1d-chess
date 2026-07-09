from g1d_chess.envs.board_mapping import BoardMapping
from g1d_chess.robots.g1d_adapter import G1DAdapter


class ChessManipulationEnv:
    def __init__(self, robot=None, board=None, arm: str = "right"):
        self.robot = robot or G1DAdapter(dry_run=True)
        self.board = board or BoardMapping()
        self.arm = arm

    def observe(self):
        return self.robot.observe()

    def execute_move(self, move: str):
        """
        Executes simple UCI moves like e2e4.
        Castling, captures, promotion, and special chess rules can be added later.
        """
        if len(move) < 4:
            raise ValueError(f"Expected UCI move like e2e4, got: {move}")

        src = move[:2]
        dst = move[2:4]

        src_xyz = self.board.square_to_xyz(src)
        dst_xyz = self.board.square_to_xyz(dst)

        print(f"[ChessManipulationEnv] move={move} src={src} {src_xyz} dst={dst} {dst_xyz}")

        self.robot.pick(src_xyz, arm=self.arm)
        self.robot.place(dst_xyz, arm=self.arm)
