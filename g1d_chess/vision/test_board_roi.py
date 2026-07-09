import argparse
import cv2

from g1d_chess.vision.board_roi_detector import BoardROIDetector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--out", default="board_roi_debug.jpg")
    parser.add_argument("--x-min", type=float, default=0.10)
    parser.add_argument("--x-max", type=float, default=0.82)
    parser.add_argument("--y-min", type=float, default=0.48)
    parser.add_argument("--y-max", type=float, default=0.98)
    args = parser.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        raise FileNotFoundError(args.image)

    detector = BoardROIDetector(
        x_min=args.x_min,
        x_max=args.x_max,
        y_min=args.y_min,
        y_max=args.y_max,
    )

    debug = detector.debug_draw(image)
    cv2.imwrite(args.out, debug)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
