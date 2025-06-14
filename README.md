# ButtBot Vision Stack

## Quick Start
1. `./env_setup.sh`
2. `python calib/capture_checker.py`
3. `python calib/homography.py`
4. `python src/butt_detector.py`    # producer
5. `python src/arm_listener.py`     # consumer

## Performance Tips
- Use a Jetson Nano or GPU device for best inference speed.
- If frame rate falls below 10 FPS, the detector automatically switches to a smaller image size.

## Common Errors
- *Camera not found*: check `/dev/video0` exists or adjust the device index.
- *ZeroMQ bind failure*: ensure no other process is using the specified port.
- *Serial connection errors*: update `SERIAL_PORT` in `src/arm_listener.py`.

## Tuning Parameters
- Detection thresholds are defined in `src/butt_detector.py`.
- Blob detection HSV ranges live in `src/fallback_blob.py`.
- Arm movement heights such as `HOVER_Z` are set at the top of `src/arm_listener.py`.
