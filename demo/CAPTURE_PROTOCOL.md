# Capture Protocol v0.1

## Purpose

This protocol defines a repeatable, privacy-conscious capture process for the cable-routing and connector-insertion demonstrator.

## 1. Pre-capture readiness

Before recording begins, confirm:

- the task and success condition are written down,
- the participant has received the task instruction,
- the capture area contains no names, screens, documents or unrelated confidential objects,
- audio recording is disabled,
- the participant's face is outside both camera views unless explicitly required,
- object and environment variants are assigned before the episode,
- camera mounts cannot move during the capture block,
- calibration files correspond to the current camera setup,
- local storage has sufficient free capacity,
- the episode identifier has not been used before.

## 2. Camera layout

### Camera 0 — operator-side view

Purpose:

- observe hand approach,
- cable grasp,
- routing path,
- connector alignment.

### Camera 1 — task-side view

Purpose:

- observe both guides,
- connector orientation,
- insertion depth,
- seated-state verification.

Both cameras should show the complete task area with minimal irrelevant background.

## 3. Calibration

Calibration must be repeated when:

- a camera is moved,
- focus or zoom changes materially,
- the task fixture moves relative to the cameras,
- a different resolution is used.

Record:

- image width and height,
- camera matrix,
- distortion coefficients,
- calibration target type and dimensions,
- number of accepted calibration frames,
- mean reprojection error,
- calibration date and operator.

The v0.1 target for mean reprojection error is **1.0 pixel or lower**. A higher value does not automatically invalidate the full project, but it must be disclosed and the affected episodes must be reviewed.

## 4. Episode start

For every episode:

1. generate or assign an `episode_id`,
2. select `participant_id`, object variant and start-position variant,
3. select intended episode class: standard success, variation, intentional failure or recovery,
4. start both camera streams,
5. wait two seconds without touching the task,
6. state no verbal information; audio remains disabled,
7. begin the task after a visible start cue,
8. stop only after the end state is visible for two seconds.

## 5. Task instruction

Base instruction:

> Pick up the cable, route it through guide one and guide two, align the connector, insert it fully and verify that it is seated.

For intentional failure and recovery episodes, use a separate written instruction that defines the permitted error state without encouraging unsafe movement.

## 6. Variations

The first sample should vary one or two controlled factors per episode:

- cable start position,
- cable curvature or slack,
- connector orientation,
- guide spacing,
- object variant,
- neutral lighting variation,
- participant.

Do not change many factors simultaneously in the first sample. The variation matrix should preserve the ability to explain what changed.

## 7. Failure and recovery capture

A failure episode must record:

- the intended failure class,
- the actual observed failure class,
- the phase where the failure occurred,
- whether a recovery was attempted,
- whether the final task succeeded,
- any safety or protocol deviation.

A recovery episode must begin from a documented error state and include:

- error-state identifier,
- first recovery action,
- number of corrective actions,
- final outcome.

## 8. Immediate quality check

After each episode, confirm:

- both video files open,
- timestamp files exist,
- the complete task is visible,
- there is no unintended face, screen or name exposure,
- no camera moved,
- intended variations match the metadata,
- final task outcome is visible,
- the episode can be accepted, conditionally accepted or rejected.

Do not postpone all quality review until the end of the capture day.

## 9. Reject reasons

Use one or more explicit reject reasons:

- `missing_camera_stream`
- `corrupt_video`
- `timestamp_gap`
- `task_out_of_frame`
- `camera_moved`
- `privacy_exposure`
- `wrong_task_instruction`
- `variation_metadata_wrong`
- `outcome_not_visible`
- `unsafe_or_unplanned_action`
- `other`

## 10. Storage and privacy

- Store identity records separately from episode data.
- Customer-facing data uses only pseudonymous participant IDs.
- Encrypt local storage and backups.
- Do not upload raw participant data to public repositories.
- Define a raw-data retention period before capture.
- Record deletion completion and exceptions.

## 11. End-of-block review

At the end of every capture block, produce:

- number of recorded episodes,
- accepted, conditional and rejected counts,
- failure and recovery coverage,
- camera/calibration incidents,
- privacy incidents,
- missing variants,
- re-capture list.

## Known limitation

Ordinary USB cameras and software timestamps cannot guarantee industrial-grade synchronization. The demonstrator must report observed timing behavior and must not describe it as hardware-synchronized.