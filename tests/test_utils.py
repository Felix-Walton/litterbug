"""Unit tests for utils helper functions."""

import math
from unittest import mock
import sys, os
os.chdir(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.getcwd())

import numpy as np

import src.utils as utils


def test_img_to_robot_roundtrip() -> None:
    H = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    with mock.patch("src.utils._load_homography", return_value=H):
        x, y = utils.img_to_robot(0.0, 0.0)
    assert abs(x) <= 1
    assert abs(y) <= 1


def test_angle_from_bbox() -> None:
    angle = utils.angle_from_bbox(20, 80)
    assert math.isclose(angle, math.pi / 2, abs_tol=0.05)
