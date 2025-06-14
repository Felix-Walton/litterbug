"""ZeroMQ subscriber that commands the robotic arm via serial G-code."""

from __future__ import annotations

import json
import time
from typing import Dict

import serial  # type: ignore
import zmq

PUB_ADDRESS = "tcp://localhost:5557"
SERIAL_PORT = "/dev/ttyUSB0"  # TODO: adjust for your hardware
BAUD = 115200
HOVER_Z = 50
GRIP_Z = 5
DUMP_X = 300
DUMP_Y = 0
DUMP_Z = 0


def send_gcode(ser: serial.Serial, cmd: str) -> None:
    ser.write(f"{cmd}\n".encode())
    time.sleep(0.05)


def goto(ser: serial.Serial, x: float, y: float, z: float) -> None:
    send_gcode(ser, f"GOTO {x:.1f} {y:.1f} {z:.1f}")


def grip_open(ser: serial.Serial) -> None:
    send_gcode(ser, "GRIP OPEN")


def grip_close(ser: serial.Serial) -> None:
    send_gcode(ser, "GRIP CLOSE")


def main() -> None:
    context = zmq.Context.instance()
    sock = context.socket(zmq.SUB)
    try:
        sock.connect(PUB_ADDRESS)
        sock.setsockopt_string(zmq.SUBSCRIBE, "")
    except zmq.ZMQError as exc:
        print(f"ZeroMQ connect failed: {exc}")
        return

    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

    while True:
        msg = sock.recv_json()
        if msg.get("conf", 0.0) < 0.15:
            continue
        x = msg["x_mm"]
        y = msg["y_mm"]
        theta = msg["theta"]
        goto(ser, x, y, HOVER_Z)
        goto(ser, x, y, GRIP_Z)
        grip_close(ser)
        goto(ser, x, y, HOVER_Z)
        goto(ser, DUMP_X, DUMP_Y, HOVER_Z)
        goto(ser, DUMP_X, DUMP_Y, DUMP_Z)
        grip_open(ser)


if __name__ == "__main__":
    main()
