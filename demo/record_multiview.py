#!/usr/bin/env python3
"""Software-timestamped multi-view recorder for the v0.1 demonstrator.

This tool is deliberately simple and honest about its limitations:
- each camera is read in its own Python thread,
- timestamps use time.perf_counter_ns(),
- streams are not hardware-triggered,
- measured timing quality must be reported rather than assumed.

Example:
    python record_multiview.py \
        --camera 0 --camera 1 \
        --output ./demo_dataset/episodes/episode_0001 \
        --episode-id episode_0001 \
        --participant-id participant_demo_01

Press q in the preview window or Ctrl+C in the terminal to stop.
"""

from __future__ import annotations

import argparse
import json
import logging
import queue
import signal
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cv2


LOGGER = logging.getLogger("record_multiview")
STOP_EVENT = threading.Event()


@dataclass(frozen=True)
class FramePacket:
    camera_id: str
    frame_index: int
    timestamp_ns: int
    frame: Any


@dataclass
class StreamStats:
    camera_id: str
    source: str
    width: int = 0
    height: int = 0
    nominal_fps: float = 0.0
    frames_read: int = 0
    frames_written: int = 0
    queue_drops: int = 0
    read_failures: int = 0
    first_timestamp_ns: int | None = None
    last_timestamp_ns: int | None = None


def parse_source(raw: str) -> int | str:
    """Treat integer-looking values as camera indexes; otherwise as paths/URLs."""
    try:
        return int(raw)
    except ValueError:
        return raw


def safe_fps(capture: cv2.VideoCapture, requested_fps: float) -> float:
    measured = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    if measured > 1.0:
        return measured
    if requested_fps > 1.0:
        return requested_fps
    return 30.0


def open_capture(
    source: int | str,
    width: int | None,
    height: int | None,
    requested_fps: float,
) -> cv2.VideoCapture:
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Could not open camera source: {source!r}")

    if width:
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if height:
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if requested_fps > 0:
        capture.set(cv2.CAP_PROP_FPS, requested_fps)

    return capture


def camera_worker(
    camera_id: str,
    source: int | str,
    output_queue: queue.Queue[FramePacket],
    stats: StreamStats,
    width: int | None,
    height: int | None,
    requested_fps: float,
) -> None:
    capture: cv2.VideoCapture | None = None
    try:
        capture = open_capture(source, width, height, requested_fps)
        stats.width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        stats.height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        stats.nominal_fps = safe_fps(capture, requested_fps)

        LOGGER.info(
            "%s opened source=%r resolution=%dx%d nominal_fps=%.2f",
            camera_id,
            source,
            stats.width,
            stats.height,
            stats.nominal_fps,
        )

        frame_index = 0
        while not STOP_EVENT.is_set():
            ok, frame = capture.read()
            timestamp_ns = time.perf_counter_ns()
            if not ok or frame is None:
                stats.read_failures += 1
                if stats.read_failures >= 10:
                    raise RuntimeError(
                        f"{camera_id}: ten consecutive/accumulated read failures"
                    )
                time.sleep(0.01)
                continue

            stats.frames_read += 1
            if stats.first_timestamp_ns is None:
                stats.first_timestamp_ns = timestamp_ns
            stats.last_timestamp_ns = timestamp_ns

            packet = FramePacket(
                camera_id=camera_id,
                frame_index=frame_index,
                timestamp_ns=timestamp_ns,
                frame=frame,
            )
            frame_index += 1

            try:
                output_queue.put(packet, timeout=0.25)
            except queue.Full:
                stats.queue_drops += 1
                LOGGER.warning("%s output queue full; frame dropped", camera_id)
    except Exception:
        LOGGER.exception("Camera worker failed for %s", camera_id)
        STOP_EVENT.set()
    finally:
        if capture is not None:
            capture.release()


def make_writer(path: Path, fps: float, width: int, height: int) -> cv2.VideoWriter:
    path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"Could not open video writer: {path}")
    return writer


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_preview(frames: dict[str, Any]) -> Any | None:
    if not frames:
        return None

    ordered = [frames[key] for key in sorted(frames)]
    target_height = min(frame.shape[0] for frame in ordered)
    resized = []
    for frame in ordered:
        if frame.shape[0] != target_height:
            scale = target_height / frame.shape[0]
            frame = cv2.resize(
                frame,
                (int(frame.shape[1] * scale), target_height),
                interpolation=cv2.INTER_AREA,
            )
        resized.append(frame)
    return cv2.hconcat(resized)


def install_signal_handlers() -> None:
    def request_stop(signum: int, _frame: Any) -> None:
        LOGGER.info("Signal %s received; stopping", signum)
        STOP_EVENT.set()

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record two or more camera streams with software timestamps."
    )
    parser.add_argument(
        "--camera",
        action="append",
        required=True,
        help="Camera index or video source. Supply at least twice.",
    )
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--episode-id", required=True)
    parser.add_argument("--participant-id", required=True)
    parser.add_argument(
        "--task-id",
        default="cable_route_connector_insert_v0_1",
    )
    parser.add_argument("--capture-block-id", default="capture_block_001")
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--fps", type=float, default=30.0)
    parser.add_argument(
        "--queue-size",
        type=int,
        default=120,
        help="Maximum packets waiting to be written per shared queue.",
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Disable the live preview window.",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=0.0,
        help="Optional automatic stop duration; zero disables it.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    args = parser.parse_args()
    if len(args.camera) < 2:
        parser.error("Supply at least two --camera values.")
    if args.width <= 0 or args.height <= 0 or args.fps <= 0:
        parser.error("Width, height and FPS must be positive.")
    if args.max_seconds < 0:
        parser.error("--max-seconds cannot be negative.")
    return args


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    install_signal_handlers()
    STOP_EVENT.clear()

    output_dir: Path = args.output.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        LOGGER.error("Output directory exists and is not empty: %s", output_dir)
        return 2
    output_dir.mkdir(parents=True, exist_ok=True)

    sources = [parse_source(value) for value in args.camera]
    packet_queue: queue.Queue[FramePacket] = queue.Queue(maxsize=args.queue_size)
    stats: dict[str, StreamStats] = {}
    threads: list[threading.Thread] = []

    for index, source in enumerate(sources):
        camera_id = f"camera_{index}"
        stream_stats = StreamStats(camera_id=camera_id, source=str(source))
        stats[camera_id] = stream_stats
        thread = threading.Thread(
            target=camera_worker,
            name=f"capture-{camera_id}",
            daemon=True,
            args=(
                camera_id,
                source,
                packet_queue,
                stream_stats,
                args.width,
                args.height,
                args.fps,
            ),
        )
        threads.append(thread)
        thread.start()

    writers: dict[str, cv2.VideoWriter] = {}
    timestamp_files: dict[str, Any] = {}
    latest_frames: dict[str, Any] = {}
    session_started_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    session_start_ns = time.perf_counter_ns()

    try:
        while not STOP_EVENT.is_set():
            if args.max_seconds > 0:
                elapsed = (time.perf_counter_ns() - session_start_ns) / 1e9
                if elapsed >= args.max_seconds:
                    STOP_EVENT.set()
                    break

            try:
                packet = packet_queue.get(timeout=0.2)
            except queue.Empty:
                if not any(thread.is_alive() for thread in threads):
                    STOP_EVENT.set()
                continue

            stream_stats = stats[packet.camera_id]
            if packet.camera_id not in writers:
                actual_height, actual_width = packet.frame.shape[:2]
                stream_stats.width = actual_width
                stream_stats.height = actual_height
                writers[packet.camera_id] = make_writer(
                    output_dir / f"{packet.camera_id}.mp4",
                    stream_stats.nominal_fps or args.fps,
                    actual_width,
                    actual_height,
                )
                timestamp_files[packet.camera_id] = (
                    output_dir / f"{packet.camera_id}_timestamps.jsonl"
                ).open("w", encoding="utf-8")

            writers[packet.camera_id].write(packet.frame)
            stream_stats.frames_written += 1
            timestamp_files[packet.camera_id].write(
                json.dumps(
                    {
                        "frame_index": packet.frame_index,
                        "timestamp_ns": packet.timestamp_ns,
                        "clock": "monotonic_ns",
                    },
                    separators=(",", ":"),
                )
                + "\n"
            )
            latest_frames[packet.camera_id] = packet.frame
            packet_queue.task_done()

            if not args.no_preview and len(latest_frames) == len(sources):
                preview = build_preview(latest_frames)
                if preview is not None:
                    cv2.imshow("Physical AI multi-view capture — press q to stop", preview)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        STOP_EVENT.set()
    except Exception:
        LOGGER.exception("Recorder failed")
        STOP_EVENT.set()
        return_code = 1
    else:
        return_code = 0
    finally:
        STOP_EVENT.set()
        for thread in threads:
            thread.join(timeout=3.0)
        for handle in timestamp_files.values():
            handle.flush()
            handle.close()
        for writer in writers.values():
            writer.release()
        cv2.destroyAllWindows()

        session_ended_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        metadata = {
            "schema_version": "0.1.0",
            "episode_id": args.episode_id,
            "task_id": args.task_id,
            "participant_id": args.participant_id,
            "capture_block_id": args.capture_block_id,
            "instruction_id": "base_instruction_v0_1",
            "start_time_utc": session_started_utc,
            "end_time_utc": session_ended_utc,
            "timestamp_clock": "monotonic_ns",
            "synchronization": "software_timestamped_not_hardware_triggered",
            "streams": [asdict(stats[key]) for key in sorted(stats)],
            "recorder": {
                "opencv_version": cv2.__version__,
                "python_version": sys.version,
                "requested_width": args.width,
                "requested_height": args.height,
                "requested_fps": args.fps,
            },
            "known_limitations": [
                "Camera reads are performed in independent Python threads.",
                "Timestamps are assigned after capture.read() returns.",
                "No hardware trigger or shared camera clock is used.",
                "Cross-camera temporal alignment is approximate and must be measured.",
            ],
        }
        write_json(output_dir / "capture_session.json", metadata)

    LOGGER.info("Capture stopped. Output: %s", output_dir)
    for camera_id in sorted(stats):
        LOGGER.info("%s stats: %s", camera_id, asdict(stats[camera_id]))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
