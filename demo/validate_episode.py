#!/usr/bin/env python3
"""Validate a demonstrator episode directory.

Checks:
- JSON Schema validation for episode.json
- required file existence
- video readability and decoded frame count
- timestamp JSONL syntax, ordering and uniqueness
- frame/timestamp count agreement
- task-phase ordering
- basic rights/privacy metadata presence

The script validates data integrity. It cannot determine whether private or
confidential material is visually present; that still requires human review.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import cv2
from jsonschema import Draft202012Validator, FormatChecker


REQUIRED_EPISODE_FILES = (
    "camera_0.mp4",
    "camera_0_timestamps.jsonl",
    "camera_1.mp4",
    "camera_1_timestamps.jsonl",
    "episode.json",
    "annotations.json",
)


@dataclass
class CheckResult:
    check: str
    passed: bool
    severity: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)


class ValidationFailure(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationFailure(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationFailure(
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def validate_schema(instance: dict[str, Any], schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
    messages: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        messages.append(f"{location}: {error.message}")
    return messages


def read_timestamps(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValidationFailure(
                        f"Invalid JSONL in {path} at line {line_number}: {exc.msg}"
                    ) from exc
                if not isinstance(row, dict):
                    raise ValidationFailure(
                        f"Timestamp row {line_number} in {path} is not an object"
                    )
                if not isinstance(row.get("timestamp_ns"), int):
                    raise ValidationFailure(
                        f"Timestamp row {line_number} in {path} lacks integer timestamp_ns"
                    )
                rows.append(row)
    except FileNotFoundError as exc:
        raise ValidationFailure(f"Missing timestamp file: {path}") from exc
    return rows


def decode_video(path: Path) -> tuple[int, float, int, int]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise ValidationFailure(f"Video cannot be opened: {path}")

    frame_count = 0
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame is None or frame.size == 0:
                raise ValidationFailure(
                    f"Decoded empty frame at index {frame_count} in {path}"
                )
            frame_count += 1
    finally:
        capture.release()

    if frame_count == 0:
        raise ValidationFailure(f"Video contains no decodable frames: {path}")
    return frame_count, fps, width, height


def timing_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    timestamps = [row["timestamp_ns"] for row in rows]
    if len(timestamps) < 2:
        return {
            "timestamp_count": len(timestamps),
            "strictly_increasing": True,
            "duplicates": 0,
            "median_interval_ms": None,
            "p95_interval_ms": None,
            "duration_seconds": 0.0,
        }

    deltas = [right - left for left, right in zip(timestamps, timestamps[1:])]
    sorted_deltas = sorted(deltas)
    p95_index = min(len(sorted_deltas) - 1, math.ceil(len(sorted_deltas) * 0.95) - 1)
    duplicates = sum(1 for delta in deltas if delta == 0)
    return {
        "timestamp_count": len(timestamps),
        "strictly_increasing": all(delta > 0 for delta in deltas),
        "duplicates": duplicates,
        "median_interval_ms": statistics.median(deltas) / 1e6,
        "p95_interval_ms": sorted_deltas[p95_index] / 1e6,
        "duration_seconds": (timestamps[-1] - timestamps[0]) / 1e9,
        "first_timestamp_ns": timestamps[0],
        "last_timestamp_ns": timestamps[-1],
    }


def phase_checks(phases: Iterable[dict[str, Any]]) -> tuple[bool, list[str]]:
    messages: list[str] = []
    previous_start = -1
    previous_end = -1
    for index, phase in enumerate(phases):
        start = phase.get("start_ns")
        end = phase.get("end_ns")
        label = phase.get("phase", f"phase_{index}")
        if not isinstance(start, int) or not isinstance(end, int):
            messages.append(f"{label}: start_ns/end_ns must be integers")
            continue
        if start >= end:
            messages.append(f"{label}: start_ns must be lower than end_ns")
        if start < previous_start:
            messages.append(f"{label}: phases are not sorted by start time")
        if previous_end > start:
            messages.append(f"{label}: overlaps the preceding phase")
        previous_start = start
        previous_end = max(previous_end, end)
    return len(messages) == 0, messages


def append_result(
    results: list[CheckResult],
    check: str,
    passed: bool,
    message: str,
    *,
    severity: str = "error",
    details: dict[str, Any] | None = None,
) -> None:
    results.append(
        CheckResult(
            check=check,
            passed=passed,
            severity=severity,
            message=message,
            details=details or {},
        )
    )


def validate_episode(
    episode_dir: Path,
    schema_path: Path,
    *,
    allow_missing_annotations: bool,
) -> list[CheckResult]:
    results: list[CheckResult] = []

    required_files = list(REQUIRED_EPISODE_FILES)
    if allow_missing_annotations:
        required_files.remove("annotations.json")
    missing = [name for name in required_files if not (episode_dir / name).is_file()]
    append_result(
        results,
        "required_files",
        not missing,
        "All required files exist" if not missing else f"Missing: {', '.join(missing)}",
        details={"missing": missing},
    )

    episode_path = episode_dir / "episode.json"
    if not episode_path.is_file():
        return results

    try:
        episode = load_json(episode_path)
    except ValidationFailure as exc:
        append_result(results, "episode_json", False, str(exc))
        return results

    if not isinstance(episode, dict):
        append_result(results, "episode_json", False, "episode.json must contain an object")
        return results

    schema_errors = validate_schema(episode, schema_path)
    append_result(
        results,
        "schema_validation",
        not schema_errors,
        "episode.json matches the schema"
        if not schema_errors
        else f"{len(schema_errors)} schema error(s)",
        details={"errors": schema_errors},
    )

    streams = episode.get("streams") if isinstance(episode.get("streams"), list) else []
    append_result(
        results,
        "minimum_streams",
        len(streams) >= 2,
        f"Declared streams: {len(streams)}",
    )

    stream_timing: dict[str, dict[str, Any]] = {}
    for stream in streams:
        if not isinstance(stream, dict):
            append_result(results, "stream_definition", False, "Stream entry is not an object")
            continue
        camera_id = str(stream.get("camera_id", "unknown_camera"))
        video_path = episode_dir / str(stream.get("video_path", ""))
        timestamps_path = episode_dir / str(stream.get("timestamps_path", ""))

        try:
            decoded_frames, decoded_fps, decoded_width, decoded_height = decode_video(video_path)
            append_result(
                results,
                f"{camera_id}.video_decode",
                True,
                f"Decoded {decoded_frames} frames",
                details={
                    "decoded_frames": decoded_frames,
                    "decoded_fps": decoded_fps,
                    "decoded_width": decoded_width,
                    "decoded_height": decoded_height,
                },
            )
        except ValidationFailure as exc:
            decoded_frames = -1
            append_result(results, f"{camera_id}.video_decode", False, str(exc))

        try:
            timestamp_rows = read_timestamps(timestamps_path)
            metrics = timing_metrics(timestamp_rows)
            stream_timing[camera_id] = metrics
            append_result(
                results,
                f"{camera_id}.timestamp_order",
                bool(metrics["strictly_increasing"]),
                "Timestamps are strictly increasing"
                if metrics["strictly_increasing"]
                else "Timestamp reversal or duplicate detected",
                details=metrics,
            )
            if decoded_frames >= 0:
                difference = decoded_frames - len(timestamp_rows)
                append_result(
                    results,
                    f"{camera_id}.frame_timestamp_count",
                    difference == 0,
                    f"Decoded frames={decoded_frames}, timestamps={len(timestamp_rows)}",
                    severity="warning" if difference != 0 else "error",
                    details={"difference": difference},
                )
        except ValidationFailure as exc:
            append_result(results, f"{camera_id}.timestamps", False, str(exc))

    if len(stream_timing) >= 2:
        starts = [
            metrics.get("first_timestamp_ns")
            for metrics in stream_timing.values()
            if metrics.get("first_timestamp_ns") is not None
        ]
        if len(starts) >= 2:
            start_offset_ms = (max(starts) - min(starts)) / 1e6
            append_result(
                results,
                "cross_camera_start_offset",
                True,
                f"Observed software start offset: {start_offset_ms:.3f} ms",
                severity="info",
                details={"start_offset_ms": start_offset_ms},
            )

    phases = episode.get("task_phases")
    if isinstance(phases, list):
        phases_ok, phase_messages = phase_checks(phases)
        append_result(
            results,
            "task_phase_order",
            phases_ok,
            "Task phases are ordered and non-overlapping"
            if phases_ok
            else f"{len(phase_messages)} phase issue(s)",
            details={"issues": phase_messages},
        )

    rights_class = episode.get("rights_class")
    append_result(
        results,
        "rights_class",
        isinstance(rights_class, str) and bool(rights_class),
        f"Rights class: {rights_class!r}",
    )

    participant_id = str(episode.get("participant_id", ""))
    looks_pseudonymous = participant_id.startswith("participant_")
    append_result(
        results,
        "pseudonymous_participant_id",
        looks_pseudonymous,
        "Participant identifier follows the pseudonymous naming convention"
        if looks_pseudonymous
        else "Participant identifier does not follow participant_* convention",
    )

    append_result(
        results,
        "visual_privacy_review",
        False,
        "Human review required: verify absence of faces, names, screens and confidential material",
        severity="manual",
    )
    append_result(
        results,
        "outcome_visibility_review",
        False,
        "Human review required: verify full task and final outcome are visible",
        severity="manual",
    )

    return results


def summarize(results: list[CheckResult]) -> dict[str, Any]:
    hard_failures = [
        result
        for result in results
        if not result.passed and result.severity == "error"
    ]
    warnings = [
        result
        for result in results
        if not result.passed and result.severity == "warning"
    ]
    manual = [result for result in results if result.severity == "manual"]
    return {
        "automated_decision": "fail" if hard_failures else "pass_pending_manual_review",
        "checks": len(results),
        "hard_failures": len(hard_failures),
        "warnings": len(warnings),
        "manual_reviews_required": len(manual),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one recorded episode directory")
    parser.add_argument("episode_dir", type=Path)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).with_name("episode.schema.json"),
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional path for a JSON validation report",
    )
    parser.add_argument(
        "--allow-missing-annotations",
        action="store_true",
        help="Useful immediately after capture, before annotation is complete",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    episode_dir = args.episode_dir.resolve()
    schema_path = args.schema.resolve()

    if not episode_dir.is_dir():
        print(f"ERROR: episode directory not found: {episode_dir}", file=sys.stderr)
        return 2
    if not schema_path.is_file():
        print(f"ERROR: schema not found: {schema_path}", file=sys.stderr)
        return 2

    try:
        results = validate_episode(
            episode_dir,
            schema_path,
            allow_missing_annotations=args.allow_missing_annotations,
        )
    except ValidationFailure as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    summary = summarize(results)
    payload = {
        "episode_dir": str(episode_dir),
        "schema": str(schema_path),
        "summary": summary,
        "results": [asdict(result) for result in results],
    }

    for result in results:
        marker = "PASS" if result.passed else result.severity.upper()
        print(f"[{marker:7}] {result.check}: {result.message}")
    print(json.dumps(summary, indent=2))

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    return 1 if summary["hard_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
