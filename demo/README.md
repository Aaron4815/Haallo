# Technical Demonstrator v0.1

## Cable Routing and Connector Insertion

This demonstrator is the first public technical proof for Physical AI Data Germany. It is intentionally small and does **not** claim production readiness or validated robot-performance uplift.

## Goal

Capture and document a human demonstration task in a form that a robotics team can technically review:

1. pick up a flexible cable,
2. route it through two guides,
3. align a connector,
4. insert the connector,
5. verify the seated state,
6. include defined failure and recovery cases.

The output is not just video. Every episode receives synchronized timestamps, task phases, outcome labels, variation metadata, quality flags and provenance information.

## Demonstrator question

Can a small, repeatable workflow turn a real human manipulation task into a technically inspectable data package with:

- two timestamped camera views,
- camera calibration references,
- task-phase labels,
- success, failure and recovery metadata,
- object and environment variations,
- privacy and rights classification,
- explicit acceptance and rejection criteria?

## Minimum setup

- two USB cameras or existing smartphones/webcams,
- fixed camera mounts,
- a printed ChArUco or checkerboard calibration target,
- a simple table-top cable-routing jig,
- one cable and at least two connector/object variants,
- a computer running Python and OpenCV,
- no audio recording,
- camera framing that avoids the participant's face by default.

## Planned sample

The first internal dataset should contain **30 episodes**:

- 15 standard successful episodes,
- 5 successful episodes with changed starting position or object variant,
- 5 intentional failure episodes,
- 5 recovery episodes that begin from a defined error state.

This is a demonstration sample, not a claim about the amount of data required to train a customer model.

## Data package

```text
demo_dataset/
├── dataset_card.md
├── capture_protocol.md
├── calibration/
│   ├── camera_0_intrinsics.json
│   ├── camera_1_intrinsics.json
│   └── camera_extrinsics.json
├── participants/
│   └── participant_register_private.csv   # never delivered to a customer
├── episodes/
│   └── episode_0001/
│       ├── camera_0.mp4
│       ├── camera_0_timestamps.jsonl
│       ├── camera_1.mp4
│       ├── camera_1_timestamps.jsonl
│       ├── episode.json
│       └── annotations.json
└── quality_report.md
```

## Task phases

The v0.1 taxonomy uses the following task phases:

1. `approach_cable`
2. `grasp_cable`
3. `route_guide_1`
4. `route_guide_2`
5. `approach_connector`
6. `align_connector`
7. `insert_connector`
8. `verify_seated`
9. `recover_from_error`
10. `complete`

## Failure taxonomy

Initial failure classes:

- `missed_grasp`
- `cable_outside_guide`
- `excessive_slack`
- `connector_misaligned`
- `partial_insertion`
- `wrong_orientation`
- `verification_failed`
- `unknown_failure`

## Evidence gates

The demonstrator is considered complete only when all of the following exist:

- reproducible capture instructions,
- two recorded and timestamped views per accepted episode,
- documented calibration procedure and result,
- complete task-phase annotations,
- defined failure and recovery examples,
- episode-level quality decision with reject reasons,
- data card and known-limitations section,
- rights/provenance class for every delivered episode,
- deletion and retention rule for raw participant information.

## Current status

- [x] task selected
- [x] data schema defined
- [x] acceptance tests defined
- [x] capture protocol drafted
- [x] data-card template drafted
- [ ] physical jig assembled
- [ ] cameras selected and mounted
- [ ] calibration executed
- [ ] first ten episodes captured
- [ ] quality report published
- [ ] external robotics review completed

## Documents

- [Capture protocol](CAPTURE_PROTOCOL.md)
- [Episode schema](episode.schema.json)
- [Acceptance tests](ACCEPTANCE_TESTS.md)
- [Data-card template](DATA_CARD_TEMPLATE.md)
- [Software-timestamped multi-view recorder](record_multiview.py)

## Important limitation

The initial recorder uses software timestamps and ordinary cameras. It is suitable for validating the workflow and metadata structure, but it is not equivalent to hardware-synchronized industrial capture. Measured timing quality must be reported rather than assumed.