"""Compute homography matrix from captured checkerboard image.

Usage: python homography.py
Click four outer corners of the checkerboard starting at origin.
Matrix is saved as homography.npy.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np

IMG_PATH = Path("calib/checker_raw.jpg")


points: List[Tuple[int, int]] = []

def on_mouse(event: int, x: int, y: int, flags: int, param) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point {len(points)}: {(x, y)}")


def main() -> None:
    if not IMG_PATH.exists():
        raise FileNotFoundError(str(IMG_PATH))

    img = cv2.imread(str(IMG_PATH))
    if img is None:
        raise RuntimeError("Failed to load image")

    cv2.namedWindow("Select Corners")
    cv2.setMouseCallback("Select Corners", on_mouse)

    while True:
        disp = img.copy()
        for p in points:
            cv2.circle(disp, p, 5, (0, 255, 0), -1)
        cv2.imshow("Select Corners", disp)
        if cv2.waitKey(1) & 0xFF == 27 or len(points) >= 4:
            break

    cv2.destroyAllWindows()
    if len(points) != 4:
        print("Need exactly four points")
        sys.exit(1)

    src = np.array(points, dtype=np.float32)
    dst = np.array([(0, 0), (200, 0), (200, 200), (0, 200)], dtype=np.float32)

    H, _ = cv2.findHomography(src, dst)
    if H is None:
        raise RuntimeError("Homography computation failed")

    np.save("calib/homography.npy", H)
    print("Homography matrix:\n", H)
    sys.exit(0)


if __name__ == "__main__":
    main()
