#!/usr/bin/env python3
"""Create a schema-valid draft episode from recorder output.

The multi-view recorder writes capture_session.json plus video/timestamp files.
This utility converts those measured stream details into episode.json and an
empty annotations.json scaffold. It does not perform human annotation or visual
privacy review.

Example:
    python scaffold_episode.py ./scratch/episode_test_0001 \
        --episode-class standard_success \
        --object-variant equipment_test \
        --start-position-variant equipment_test \
        --outcome aborted
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


EPISODE_CLASSES = (
    "standard_success",
    "variation_success",
    "intentional_failure",
    "recovery",
)
OUTCOMES = ("success", "failure", "aborted")
RIGHTS_CLASSES = (
    "internal_validation_only",
    "named_customer_project",
    "nonexclusive_reuse_permitted",
)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def positive_int(value: Any, default: int = 1) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)) and value > 0:
        return int(value)
    return default


def positive_float(value: Any, default: float = 30.0) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)) and value > 0:
        return float(value)
    return default


def calculate_duration(streams: list[dict[str, Any]]) -> float:
    starts = [
        stream.get("first_timestamp_ns")
        for stream in streams
        if isinstance(stream.get("first_timestamp_ns"), int)
    ]
    ends = [
        stream.get("last_timestamp_ns")
        for stream in streams
        if isinstance(stream.get("last_timestamp_ns"), int)
    ]
    if not starts or not ends:
        return 0.0
    duration = (max(ends) - min(starts)) / 1e9
    return max(0.0, round(duration, 6))


def validate_files(episode_dir: Path, streams: list[dict[str, Any]]) -> None:
    problems: list[str] = []
    if len(streams) < 2:
        problems.append("capture_session.json declares fewer than two streams")

    for stream in streams:
        camera_id = stream.get("camera_id")
        if not isinstance(camera_id, str) or not camera_id:
            problems.append("a stream lacks camera_id")
            continue
        for filename in (f"{camera_id}.mp4", f"{camera_id}_timestamps.jsonl"):
            if not (episode_dir / filename).is_file():
                problems.append(f"missing recorder output: {filename}")

    if problems:
        raise RuntimeError("; ".join(problems))


def build_episode(args: argparse.Namespace, session: dict[str, Any]) -> dict[str, Any]:
    raw_streams = session.get("streams")
    if not isinstance(raw_streams, list):
        raise RuntimeError("capture_session.json lacks a streams array")

    validate_files(args.episode_dir, raw_streams)

    streams: list[dict[str, Any]] = []
    limitations = list(session.get("known_limitations") or [])
    calibration_state = "calibrated" if args.calibration_prefix else "uncalibrated"

    for raw in raw_streams:
        if not isinstance(raw, dict):
            raise RuntimeError("capture_session.json contains a non-object stream")
        camera_id = str(raw.get("camera_id", ""))
        calibration_id = (
            f"{args.calibration_prefix}_{camera_id}"
            if args.calibration_prefix
            else f"uncalibrated_{camera_id}"
        )
        streams.append(
            {
                "camera_id": camera_id,
                "video_path": f"{camera_id}.mp4",
                "timestamps_path": f"{camera_id}_timestamps.jsonl",
                "width": positive_int(raw.get("width")),
                "height": positive_int(raw.get("height")),
                "nominal_fps": positive_float(raw.get("nominal_fps")),
                "recorded_frames": max(0, int(raw.get("frames_written") or 0)),
                "calibration_id": calibration_id,
                "timestamp_clock": "monotonic_ns",
            }
        )

        queue_drops = int(raw.get("queue_drops") or 0)
        read_failures = int(raw.get("read_failures") or 0)
        if queue_drops:
            limitations.append(f"{camera_id} recorded {queue_drops} queue drop(s).")
        if read_failures:
            limitations.append(f"{camera_id} recorded {read_failures} read failure(s).")

    if calibration_state == "uncalibrated":
        limitations.append(
            "The camera setup is not yet linked to measured calibration files."
        )

    episode = {
        "schema_version": "0.1.0",
        "episode_id": args.episode_id or session.get("episode_id"),
        "task_id": session.get("task_id", "cable_route_connector_insert_v0_1"),
        "participant_id": args.participant_id or session.get("participant_id"),
        "capture_block_id": session.get("capture_block_id", "capture_block_unknown"),
        "episode_class": args.episode_class,
        "instruction_id": args.instruction_id,
        "start_time_utc": session.get("start_time_utc"),
        "duration_seconds": calculate_duration(raw_streams),
        "streams": streams,
        "object_variant": args.object_variant,
        "start_position_variant": args.start_position_variant,
        "environment_variants": args.environment_variant,
        "intended_failure_class": args.intended_failure_class,
        "observed_failure_classes": [],
        "recovery_attempted": args.episode_class == "recovery",
        "recovery_successful": None,
        "outcome": args.outcome,
        "task_phases": [],
        "rights_class": args.rights_class,
        "retention_class": args.retention_class,
        "quality": {
            "decision": "conditional",
            "reviewer_id": "pending_human_review",
            "reject_reasons": [],
            "notes": (
                "Automatically scaffolded from capture_session.json. "
                "Task phases, outcome, privacy and final quality require human review."
            ),
        },
        "known_limitations": sorted(set(str(item) for item in limitations if item)),
    }

    required_strings = (
        "episode_id",
        "participant_id",
        "start_time_utc",
    )
    missing = [key for key in required_strings if not isinstance(episode.get(key), str)]
    if missing:
        raise RuntimeError(f"Missing required session values: {', '.join(missing)}")

    return episode


def validate_against_schema(episode: dict[str, Any], schema_path: Path) -> None:
    schema = read_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(episode), key=lambda error: list(error.path))
    if errors:
        messages = []
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            messages.append(f"{location}: {error.message}")
        raise RuntimeError("Generated episode does not validate: " + "; ".join(messages))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create episode.json and annotations.json from capture_session.json"
    )
    parser.add_argument("episode_dir", type=Path)
    parser.add_argument("--episode-id")
    parser.add_argument("--participant-id")
    parser.add_argument("--episode-class", choices=EPISODE_CLASSES, default="standard_success")
    parser.add_argument("--instruction-id", default="base_instruction_v0_1")
    parser.add_argument("--object-variant", default="equipment_test")
    parser.add_argument("--start-position-variant", default="equipment_test")
    parser.add_argument(
        "--environment-variant",
        action="append",
        default=["controlled_indoor_demo"],
    )
    parser.add_argument("--intended-failure-class", default=None)
    parser.add_argument("--outcome", choices=OUTCOMES, default="aborted")
    parser.add_argument(
        "--rights-class",
        choices=RIGHTS_CLASSES,
        default="internal_validation_only",
    )
    parser.add_argument("--retention-class", default="equipment_test_delete_after_review")
    parser.add_argument(
        "--calibration-prefix",
        help="Prefix for real calibration IDs. Omit for an explicitly uncalibrated draft.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).with_name("episode.schema.json"),
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.episode_dir = args.episode_dir.resolve()
    args.schema = args.schema.resolve()

    if not args.episode_dir.is_dir():
        print(f"ERROR: episode directory not found: {args.episode_dir}")
        return 2

    episode_path = args.episode_dir / "episode.json"
    annotations_path = args.episode_dir / "annotations.json"
    if not args.force and (episode_path.exists() or annotations_path.exists()):
        print("ERROR: episode.json or annotations.json already exists; use --force to replace")
        return 2

    try:
        session = read_json(args.episode_dir / "capture_session.json")
        if not isinstance(session, dict):
            raise RuntimeError("capture_session.json must contain an object")
        episode = build_episode(args, session)
        validate_against_schema(episode, args.schema)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 1

    annotations = {
        "schema_version": "0.1.0",
        "episode_id": episode["episode_id"],
        "status": "pending_human_annotation",
        "task_phases": [],
        "observed_failure_classes": [],
        "notes": [
            "This scaffold is not a completed annotation.",
            "Visual privacy and outcome review are still required."
        ],
    }

    write_json(episode_path, episode)
    write_json(annotations_path, annotations)
    print(f"Created {episode_path}")
    print(f"Created {annotations_path}")
    print("Schema validation passed. Manual annotation and review remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
