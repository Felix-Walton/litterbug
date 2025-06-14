"""Utility functions for coordinate transforms and angles."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import cv2
import numpy as np

HOMOGRAPHY_PATH = Path("calib/homography.npy")


def _load_homography() -> np.ndarray:
    if not HOMOGRAPHY_PATH.exists():
        raise FileNotFoundError(str(HOMOGRAPHY_PATH))
    return np.load(str(HOMOGRAPHY_PATH))


def img_to_robot(cx: float, cy: float) -> Tuple[float, float]:
    """Convert pixel coordinates to millimetres using cached homography."""
    H = _load_homography()
    pt = np.array([[cx, cy, 1.0]], dtype=float).T
    world = H @ pt
    world /= world[2, 0]
    return float(world[0, 0]), float(world[1, 0])


def angle_from_bbox(w: float, h: float) -> float:
    """Return object orientation in radians using bounding box."""
    return float(np.pi/2) if h > w else 0.0


def mask_principal_angle(mask: np.ndarray) -> float:
    """Return principal axis angle of binary mask in radians."""
    coords = cv2.findNonZero(mask)
    if coords is None:
        return 0.0
    mean, eigvecs = cv2.PCACompute(coords.astype(np.float32), mean=None)[:2]
    vec = eigvecs[0]
    return float(np.arctan2(vec[1], vec[0]))
