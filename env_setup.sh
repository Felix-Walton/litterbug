#!/usr/bin/env bash
python3 -m venv buttbot-env \
  && source buttbot-env/bin/activate \
  && pip install -U pip wheel \
  && pip install "ultralytics==8.3.1" "fastsam==1.0.3" \
                 pyzmq opencv-python numpy pytest

# Download YOLO-World weights
mkdir -p models && \
wget -O models/yolo_world_s.pt \
  https://huggingface.co/AILab-CVC/yolo-world/resolve/main/yolo_world_s.pt
