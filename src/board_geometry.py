FILES = "abcdefgh"
RANKS = "12345678"

def square_to_xy(square, config):
    board_cfg = config["board"]

    square_size = board_cfg["square_size_m"]
    origin_x = board_cfg["origin_x_m"]
    origin_y = board_cfg["origin_y_m"]

    file_char = square[0]
    rank_char = square[1]

    x = FILES.index(file_char) * square_size + origin_x
    y = RANKS.index(rank_char) * square_size + origin_y

    return x, y

def move_to_pick_place(move_uci, config):
    from_square = move_uci[:2]
    to_square = move_uci[2:4]

    return {
        "move": move_uci,
        "from": from_square,
        "to": to_square,
        "pick_xy": square_to_xy(from_square, config),
        "place_xy": square_to_xy(to_square, config),
    }
