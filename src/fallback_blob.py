"""HSV blob detector used when VLM confidence is low."""

from __future__ import annotations

from typing import Any, Dict

import cv2
import numpy as np
import zmq

from . import utils

PUB_ADDRESS = "tcp://*:5558"
LOW_CONF = 0.1

ORANGE_LOW = (5, 50, 50)
ORANGE_HIGH = (20, 255, 255)
WHITE_LOW = (0, 0, 200)
WHITE_HIGH = (180, 60, 255)


def main() -> None:
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

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_o = cv2.inRange(hsv, ORANGE_LOW, ORANGE_HIGH)
        mask_w = cv2.inRange(hsv, WHITE_LOW, WHITE_HIGH)
        mask = cv2.bitwise_or(mask_o, mask_w)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 300:
                continue
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            x_mm, y_mm = utils.img_to_robot(cx, cy)
            msg = {"x_mm": x_mm, "y_mm": y_mm, "theta": 0.0, "conf": LOW_CONF, "source": "blob"}
            sock.send_json(msg)
        cv2.imshow("blob", mask)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
