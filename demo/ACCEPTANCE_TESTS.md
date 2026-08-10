# Acceptance Tests v0.1

## Purpose

These tests define when an episode and the demonstrator package are technically reviewable. They are not a guarantee that a dataset improves a robot model.

## A. Episode-level hard requirements

An episode must be rejected when any hard requirement fails.

### A1. Required files

The episode directory contains:

- `camera_0.mp4`
- `camera_0_timestamps.jsonl`
- `camera_1.mp4`
- `camera_1_timestamps.jsonl`
- `episode.json`
- `annotations.json`

**Pass:** every required file exists and can be opened.

### A2. Stream completeness

- At least two camera streams are declared in `episode.json`.
- Every declared video has a timestamp file.
- Recorded frame count is greater than zero.

**Pass:** all declared streams are present and non-empty.

### A3. Timestamp integrity

For every stream:

- timestamps are integers in nanoseconds,
- timestamps are strictly increasing,
- duplicate timestamps are not permitted,
- timestamp row count equals decoded frame count, or the discrepancy is explicitly documented and the episode is conditionally accepted.

**Pass:** no reversal or duplicate; frame/timestamp discrepancy is zero for normal acceptance.

### A4. Visual task coverage

At least one stream must clearly show each of the following:

- initial cable position,
- both cable guides,
- connector and receiving interface,
- grasp,
- routing through both guides,
- alignment,
- insertion attempt,
- final outcome.

**Pass:** no mandatory event occurs entirely outside all camera views.

### A5. Outcome visibility

The final state remains visible long enough to decide whether the connector is seated.

**Pass:** outcome is unambiguous to the reviewer.

### A6. Metadata validity

`episode.json` validates against `episode.schema.json`.

**Pass:** zero schema errors.

### A7. Rights and privacy

- `rights_class` is present.
- Participant identity is not stored inside the delivered episode directory.
- No unintended face, name, screen, document or unrelated confidential material is visible.

**Pass:** rights class is valid and privacy review finds no exposure.

## B. Conditional requirements

A failure here may produce a conditional acceptance if the limitation is useful and documented.

### B1. Calibration

The episode references the calibration identifier used for both cameras.

Target:

- mean reprojection error at or below 1.0 pixel for each camera.

If the target is exceeded:

- disclose the measured value,
- review whether the episode is still useful for 2D-only analysis,
- do not claim precise 3D reconstruction quality.

### B2. Software timing quality

For software-timestamped cameras:

- report nominal FPS,
- report median inter-frame interval,
- report p95 inter-frame interval,
- report dropped or missing timestamps,
- estimate cross-camera start offset.

No unsupported claim of hardware synchronization is permitted.

### B3. Task-phase coverage

Accepted successful episodes should contain:

1. `approach_cable`
2. `grasp_cable`
3. `route_guide_1`
4. `route_guide_2`
5. `approach_connector`
6. `align_connector`
7. `insert_connector`
8. `verify_seated`
9. `complete`

Recovery episodes additionally contain `recover_from_error`.

### B4. Annotation ordering

For each annotated phase:

- `start_ns < end_ns`,
- phases do not overlap unless the overlap is explicitly allowed,
- phase order is physically plausible.

## C. Dataset-level acceptance

The 30-episode v0.1 sample passes only if:

- at least 27 episodes are accepted or conditionally accepted,
- all four planned episode classes are represented,
- at least five intentional failures are present,
- at least five recovery episodes are present,
- every declared object/start-position variant appears in the variation matrix,
- 100% of delivered episodes have a valid rights class,
- 100% of rejected episodes have at least one reject reason,
- the data card and quality report describe known limitations,
- no private participant register is included in the public or customer-facing package.

## D. Quality metrics to report

```text
recorded_episodes
accepted_episodes
conditional_episodes
rejected_episodes
acceptance_rate
rework_rate
stream_completeness_rate
timestamp_integrity_rate
privacy_pass_rate
rights_metadata_rate
failure_class_coverage
recovery_success_rate
median_episode_duration_seconds
median_inter_frame_interval_ms_by_camera
p95_inter_frame_interval_ms_by_camera
```

## E. Review procedure

1. Run automated schema and file checks.
2. Decode every video at least once to verify readability.
3. Perform full human review for all v0.1 episodes.
4. Record decision and reject reasons in `episode.json`.
5. Re-capture rejected mandatory variants.
6. Publish aggregate metrics in `quality_report.md`.

## F. Explicit non-claims

Passing these tests does not establish:

- robot-policy improvement,
- cross-robot transfer,
- industrial safety certification,
- hardware-level synchronization,
- statistically representative worker behavior,
- suitability for a customer's production deployment.

Those claims require customer-specific testing and separate evidence.