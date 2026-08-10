#!/usr/bin/env bash
set -euo pipefail

# One-command equipment dry run for macOS/Linux.
# Usage:
#   bash run_mac_dry_test.sh [camera_0] [camera_1] [duration_seconds]
# Example:
#   bash run_mac_dry_test.sh 0 1 10
#
# This script records equipment-test footage only. It does not establish a
# legal basis for recording workers and does not claim hardware synchronization.

CAMERA_0="${1:-0}"
CAMERA_1="${2:-1}"
DURATION="${3:-10}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is not installed or not on PATH." >&2
  exit 2
fi

if [[ ! "$DURATION" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  echo "ERROR: duration must be a positive number of seconds." >&2
  exit 2
fi

if [[ ! -d .venv ]]; then
  echo "Creating Python virtual environment..."
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt >/dev/null

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
EPISODE_ID="episode_equipment_${STAMP}"
OUTPUT_DIR="$SCRIPT_DIR/scratch/$EPISODE_ID"

cat <<EOF

Physical AI Data Germany — equipment dry run
Camera 0: $CAMERA_0
Camera 1: $CAMERA_1
Duration: $DURATION seconds
Output:   $OUTPUT_DIR

Important:
- Grant camera access to Terminal/Python in macOS System Settings.
- Keep faces, names, screens and confidential material outside both views.
- Audio is not recorded by this tool.
- The streams are software timestamped, not hardware synchronized.
EOF

echo "\n1/4 Probing local cameras..."
python list_cameras.py || {
  echo "ERROR: No camera produced a frame during discovery." >&2
  exit 1
}

echo "\n2/4 Recording two-camera equipment test..."
python record_multiview.py \
  --camera "$CAMERA_0" \
  --camera "$CAMERA_1" \
  --output "$OUTPUT_DIR" \
  --episode-id "$EPISODE_ID" \
  --participant-id participant_equipment_test \
  --capture-block-id "capture_block_${STAMP}" \
  --max-seconds "$DURATION"

echo "\n3/4 Creating schema-valid draft episode metadata..."
python scaffold_episode.py "$OUTPUT_DIR" \
  --episode-class standard_success \
  --object-variant equipment_test \
  --start-position-variant equipment_test \
  --outcome aborted \
  --rights-class internal_validation_only \
  --retention-class equipment_test_delete_after_review

echo "\n4/4 Running automated integrity validation..."
python validate_episode.py "$OUTPUT_DIR" \
  --report "$OUTPUT_DIR/validation_report.json"

cat <<EOF

Dry run completed.

Review these measured files:
  $OUTPUT_DIR/capture_session.json
  $OUTPUT_DIR/episode.json
  $OUTPUT_DIR/validation_report.json

Then manually verify:
- no face, name, screen, document or confidential material is visible,
- both views show the intended task area,
- the final state is visible,
- no unsafe or unplanned action occurred.

Do not publish raw videos or participant data automatically.
EOF
