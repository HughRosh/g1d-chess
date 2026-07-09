import argparse
import cv2

from g1d_chess.vision.yolo_detector import YOLOChessDetector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--out", default="yolo_debug.jpg")
    args = parser.parse_args()

    detector = YOLOChessDetector(args.model)
    detections = detector.detect(args.image)

    image = cv2.imread(args.image)
    if image is None:
        raise FileNotFoundError(args.image)

    for det in detections:
        x1, y1, x2, y2 = map(int, det.xyxy)
        label = f"{det.label} {det.confidence:.2f}"

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image,
            label,
            (x1, max(y1 - 8, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        print(det)

    cv2.imwrite(args.out, image)
    print(f"Saved {args.out}")


if __name__ == "__main__":
    main()
