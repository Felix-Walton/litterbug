"""Vision producer that detects cigarette butts and publishes positions."""

from __future__ import annotations

import sys
import time
from typing import Any, Dict

import cv2
import numpy as np
import zmq

from ultralytics import YOLO

from . import utils

MODEL = "models/yolo_world_s.pt"
PROMPTS = ["cigarette butt", "cigarette filter"]
CONF_THRES = 0.25
PUB_ADDRESS = "tcp://*:5557"


def main() -> None:
    """Run detection loop and publish over ZeroMQ."""
    try:
        detector = YOLO(MODEL)
    except Exception as exc:
        print(f"Failed to load model: {exc}")
        sys.exit(1)

    context = zmq.Context.instance()
    sock = context.socket(zmq.PUB)
    try:
        sock.bind(PUB_ADDRESS)
    except zmq.ZMQError as exc:
        print(f"ZeroMQ bind failed: {exc}")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera")

    imgsz = 640
    while True:
        t0 = time.time()
        ret, frame = cap.read()
        if not ret:
            continue

                results = detector.predict(frame, imgsz=imgsz, classes=PROMPTS, conf=CONF_THRES)
        msg: Dict[str, Any] = {}
        if results[0].boxes:
            box = results[0].boxes[0]
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
            conf = float(box.conf[0])
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            w = x2 - x1
            h = y2 - y1
            x_mm, y_mm = utils.img_to_robot(cx, cy)
            theta = utils.angle_from_bbox(w, h)
            msg = {"x_mm": x_mm, "y_mm": y_mm, "theta": theta, "conf": conf}
            sock.send_json(msg)
        cv2.imshow("detector", annotated)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        fps = 1.0 / max(time.time() - t0, 1e-6)
        if fps < 10 and imgsz != 320:
            imgsz = 320
            print("Performance low, switching to imgsz=320")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
