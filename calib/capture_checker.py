"""Capture checkerboard image for homography calibration.

Usage: python capture_checker.py
Press SPACE to capture and save checker_raw.jpg.
Press ESC to quit without saving.
"""

import cv2


def main() -> None:
    """Open camera and capture checkerboard image."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open /dev/video0")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            cv2.imshow("Checker Capture", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            if key == 32:  # SPACE
                cv2.imwrite("calib/checker_raw.jpg", frame)
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
