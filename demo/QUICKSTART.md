# Demonstrator Quickstart

## 1. Clone and create an environment

```bash
git clone https://github.com/Aaron4815/Haallo.git
cd Haallo/demo
python -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2. Check camera indexes

The recorder accepts integer camera indexes or video sources. Common local indexes are `0` and `1`, but this varies by computer.

Start with:

```bash
python record_multiview.py --help
```

Do not begin a participant capture until both views, storage location and privacy framing have been checked.

## 3. Record a short equipment test

Create an empty output directory automatically by giving a new episode path:

```bash
python record_multiview.py \
  --camera 0 \
  --camera 1 \
  --output ./scratch/episode_test_0001 \
  --episode-id episode_test_0001 \
  --participant-id participant_equipment_test \
  --max-seconds 10
```

On Windows PowerShell, write the command on one line or use the PowerShell continuation character.

The recorder writes:

- one MP4 per camera,
- one timestamp JSONL file per camera,
- `capture_session.json` with measured stream statistics and limitations.

The equipment test is not yet a valid dataset episode. It confirms only that streams can be captured and decoded.

## 4. Inspect timing statistics

Review `capture_session.json` for:

- actual resolution,
- nominal FPS,
- frames read and written,
- queue drops,
- read failures,
- first and last timestamp,
- documented software-synchronization limitation.

Do not describe the result as hardware-synchronized.

## 5. Prepare a valid episode directory

For a fully reviewable episode, add:

```text
episode.json
annotations.json
```

Use:

- `episode.schema.json` as the formal schema,
- `example_episode.json` as a metadata example,
- `CAPTURE_PROTOCOL.md` for the capture procedure,
- `ACCEPTANCE_TESTS.md` for the quality decision.

The metadata paths in `episode.json` must match the actual filenames.

## 6. Validate an episode

```bash
python validate_episode.py ./demo_dataset/episodes/episode_0001 \
  --report ./demo_dataset/episodes/episode_0001/validation_report.json
```

Immediately after capture, before annotation is complete:

```bash
python validate_episode.py ./scratch/episode_test_0001 \
  --allow-missing-annotations
```

A successful automated run returns:

```text
pass_pending_manual_review
```

Human review remains mandatory for:

- unintended faces or identifiers,
- screens, documents and confidential material,
- complete task visibility,
- unambiguous final outcome,
- safety/protocol deviations.

## 7. Validate the example metadata only

```bash
python - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

schema = json.loads(Path("episode.schema.json").read_text())
example = json.loads(Path("example_episode.json").read_text())
Draft202012Validator.check_schema(schema)
Draft202012Validator(schema, format_checker=FormatChecker()).validate(example)
print("Example metadata is valid.")
PY
```

## 8. Before recording real people

The repository does not itself provide a sufficient legal basis for recording workers. Before any real participant capture, define and review:

- purpose and recipient,
- controller/processor roles,
- participant information and legal basis,
- employer and works-council involvement where applicable,
- compensation and voluntariness,
- allowed reuse,
- retention and deletion,
- access and encryption,
- incident handling.

Start with staged, voluntary demonstrations in a controlled area. Do not record normal work shifts as the first test.

## 9. Definition of v0.1 completion

The public technical demonstrator is complete only after:

- the physical jig exists,
- calibration results are published,
- at least ten real internal test episodes are captured,
- automated checks pass,
- human privacy/quality review is complete,
- aggregate quality metrics are published,
- known limitations are explicit,
- an external robotics practitioner reviews the package.
