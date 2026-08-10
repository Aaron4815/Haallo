#!/usr/bin/env python3
"""Discover locally available OpenCV camera indexes.

The result is a best-effort equipment check. A camera that opens here may still
fail under sustained multi-camera recording because of bandwidth, drivers,
permissions or resolution settings.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from dataclasses import asdict, dataclass

import cv2


@dataclass
class CameraProbe:
    index: int
    opened: bool
    frame_read: bool
    width: int | None = None
    height: int | None = None
    nominal_fps: float | None = None
    backend: str | None = None
    error: str | None = None


def probe_camera(index: int, warmup_seconds: float) -> CameraProbe:
    capture = cv2.VideoCapture(index)
    if not capture.isOpened():
        capture.release()
        return CameraProbe(index=index, opened=False, frame_read=False)

    try:
        if warmup_seconds > 0:
            deadline = time.monotonic() + warmup_seconds
            while time.monotonic() < deadline:
                capture.grab()

        ok, frame = capture.read()
        backend = None
        try:
            backend = capture.getBackendName()
        except Exception:
            backend = None

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0) or None
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0) or None
        fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0) or None

        if ok and frame is not None:
            height, width = frame.shape[:2]

        return CameraProbe(
            index=index,
            opened=True,
            frame_read=bool(ok and frame is not None),
            width=width,
            height=height,
            nominal_fps=fps,
            backend=backend,
        )
    except Exception as exc:
        return CameraProbe(
            index=index,
            opened=True,
            frame_read=False,
            error=f"{type(exc).__name__}: {exc}",
        )
    finally:
        capture.release()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe local OpenCV camera indexes and print a JSON report."
    )
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int, default=9)
    parser.add_argument("--warmup-seconds", type=float, default=0.2)
    parser.add_argument("--json", action="store_true", help="Print JSON only")
    args = parser.parse_args()
    if args.start < 0 or args.end < args.start:
        parser.error("Require 0 <= --start <= --end")
    if args.warmup_seconds < 0:
        parser.error("--warmup-seconds cannot be negative")
    return args


def main() -> int:
    args = parse_args()
    results = [
        probe_camera(index, args.warmup_seconds)
        for index in range(args.start, args.end + 1)
    ]
    available = [result for result in results if result.frame_read]

    payload = {
        "platform": platform.platform(),
        "opencv_version": cv2.__version__,
        "probed_indexes": [args.start, args.end],
        "available_camera_indexes": [result.index for result in available],
        "results": [asdict(result) for result in results],
        "limitations": [
            "This is a short best-effort probe, not a sustained recording test.",
            "Camera permissions may need to be granted to the terminal or Python runtime.",
            "Two cameras can open individually and still exceed USB bandwidth together.",
        ],
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"OpenCV {cv2.__version__} on {platform.system()}")
        if available:
            print("Available cameras:")
            for result in available:
                print(
                    f"  index={result.index} "
                    f"resolution={result.width}x{result.height} "
                    f"fps={result.nominal_fps} backend={result.backend}"
                )
        else:
            print("No camera produced a frame in the probed range.")
        print("\nFull JSON report:")
        print(json.dumps(payload, indent=2))

    return 0 if available else 1


if __name__ == "__main__":
    raise SystemExit(main())
