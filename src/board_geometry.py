FILES = "abcdefgh"
RANKS = "12345678"

def square_to_xy(square, square_size=0.05, origin_x=0.0, origin_y=0.0):
    """
    Convert chess square like 'e2' into board x/y coordinates in meters.
    Default square size = 0.05 m = 5 cm.
    origin is a1.
    """
    file_char = square[0]
    rank_char = square[1]

    x = FILES.index(file_char) * square_size + origin_x
    y = RANKS.index(rank_char) * square_size + origin_y

    return x, y

def move_to_pick_place(move_uci):
    from_square = move_uci[:2]
    to_square = move_uci[2:4]

    pick_xy = square_to_xy(from_square)
    place_xy = square_to_xy(to_square)

    return {
        "move": move_uci,
        "from": from_square,
        "to": to_square,
        "pick_xy": pick_xy,
        "place_xy": place_xy,
    }
