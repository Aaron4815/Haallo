# Demonstrator Specification

## Cable Routing & Connector Insertion v0.1

**Status:** design specification — not yet a completed production dataset  
**Purpose:** demonstrate that the planned data operation can convert a defined manual task into calibrated, reviewable and rights-aware robotics data.

## 1. Task

A participant shall:

1. identify and reach for a flexible cable,
2. grasp it at a permitted grip region,
3. route it through two defined guides,
4. orient the connector relative to the socket,
5. insert the connector,
6. verify the seated state,
7. recover from a controlled failure when instructed.

The demonstrator is not intended to prove universal robot-policy improvement. It is intended to prove capture quality, task structure, variation coverage, QA and provenance.

## 2. Task phases

| Phase | Definition | Required labels |
|---|---|---|
| `approach` | Hand moves toward the cable | start/end, active hand |
| `grasp` | Stable cable acquisition | grasp point, success/failure |
| `route_1` | Cable passes guide 1 | guide contact, snag/slip |
| `route_2` | Cable passes guide 2 | guide contact, snag/slip |
| `align` | Connector is oriented to socket | relative pose, correction count |
| `insert` | Connector enters socket | first contact, insertion depth/state |
| `verify` | Seated state is checked | verification method, result |
| `recover` | Participant corrects a controlled error | trigger, recovery strategy, outcome |

## 3. Planned capture modalities

### Mandatory

- calibrated overhead RGB camera,
- calibrated oblique RGB camera,
- shared hardware or software timestamp reference,
- task-state and event annotations,
- object/fixture geometry reference,
- per-episode rights and QA metadata.

### Preferred

- RGB-D camera covering the work volume,
- 2D/3D hand keypoints,
- connector and socket pose estimates,
- cable centerline or control-point representation,
- fixture state and verification signal.

### Optional, customer-driven

- wrist/egocentric camera,
- IMU,
- force/torque or instrumented fixture data,
- teleoperation or robot action-state logs.

No optional modality is collected merely because it is available. It must support a defined customer decision or benchmark.

## 4. Initial variation matrix

| Dimension | Initial values |
|---|---|
| Cable type | 2 flexible cable variants |
| Connector | 2 connector/socket variants |
| Start position | 5 defined positions |
| Connector orientation | 4 orientations |
| Routing condition | nominal, mild snag, mis-route |
| Lighting | nominal, reduced contrast |
| Outcome | success, failure, successful recovery, failed recovery |

The matrix is illustrative and will be frozen only after a customer or technical reviewer confirms relevance.

## 5. Planned episode mix

For the first internal technical sample:

- 30–50 total episodes,
- approximately 60% nominal success,
- approximately 20% controlled failures,
- approximately 20% recovery sequences,
- no continuous workplace recording,
- no production-worker performance measurement.

## 6. Calibration and synchronization

Planned procedure:

1. record a calibration target visible to all cameras,
2. estimate intrinsics and distortion per camera,
3. estimate camera-to-workcell extrinsics,
4. record a synchronization event visible to all streams,
5. store calibration and synchronization reports with the dataset,
6. repeat checks after any camera or fixture movement.

Initial target thresholds for technical review:

- median reprojection error: ≤ 1.5 pixels,
- maximum inter-stream timestamp offset: ≤ 15 ms,
- mandatory-stream completeness: ≥ 95%,
- calibration provenance present for 100% of accepted episodes.

These are engineering targets, not already achieved results.

## 7. Annotation

Each accepted episode should include:

- task and episode ID,
- instruction,
- variant values,
- phase intervals,
- contact and state-change events,
- success/failure/recovery outcome,
- controlled-failure trigger where applicable,
- quality status and rejection reasons,
- rights/provenance class.

A sample machine-readable schema is provided at [`schemas/episode.schema.json`](../schemas/episode.schema.json).

## 8. Acceptance logic

An episode is accepted only when:

- every mandatory stream is present and readable,
- calibration references are valid,
- synchronization meets the project threshold,
- mandatory task phases can be identified,
- the outcome label is defensible,
- rights/provenance fields are complete,
- no prohibited personal or confidential content is present.

Rejected episodes retain a structured reject reason but are not delivered as accepted training data.

## 9. Privacy and workplace boundaries

The first demonstrator uses a staged workbench, not an ordinary employee shift.

- no covert recording,
- no continuous performance monitoring,
- no audio by default,
- camera framing avoids faces and name identifiers,
- participant identity is separated from dataset identifiers,
- reuse beyond the defined demonstrator requires a separate rights basis,
- raw-data retention is time-limited and documented.

## 10. Planned deliverables

- synchronized videos,
- calibration files and report,
- episode metadata conforming to the JSON schema,
- phase and event annotations,
- optional trajectories where quality is sufficient,
- data card,
- QA report,
- rights/provenance matrix,
- list of known limitations.

## 11. Technical review request

A useful reviewer should challenge:

1. whether human demonstrations are the correct modality,
2. whether object-centric trajectories or robot action-state data are required,
3. whether the variation matrix reflects real deployment failures,
4. whether the acceptance thresholds are meaningful,
5. which benchmark would determine downstream utility.

Contact: **Aaron Wißmann — aaronwiss62@gmail.com**