# Data Card — Cable Routing and Connector Insertion

> Template for the v0.1 demonstrator. Replace every bracketed field before external delivery.

## 1. Dataset identity

| Field | Value |
|---|---|
| Dataset name | Physical AI Cable Routing and Connector Insertion Demo |
| Version | [0.1.0] |
| Release date | [YYYY-MM-DD] |
| Owner | [Legal entity / project owner] |
| Contact | [Operational and privacy contact] |
| Task ID | `cable_route_connector_insert_v0_1` |
| License / contractual use | [Named-customer / internal-validation / permitted reuse] |

## 2. Executive description

This dataset contains human demonstrations of a table-top cable-routing and connector-insertion task. Episodes include two camera views, software timestamps, task-phase annotations, task variations, outcomes, defined failure classes, recovery behavior, quality decisions and provenance metadata.

The dataset is intended to test the data-production workflow and to support technical review. It does not by itself demonstrate improvement of a robot policy.

## 3. Intended uses

Permitted intended uses must be stated precisely, for example:

- internal evaluation of human-demonstration data formats,
- development of object- and task-state representations,
- testing of annotation and quality pipelines,
- customer-specific feasibility evaluation,
- research into failure and recovery classification.

## 4. Out-of-scope and prohibited uses

Unless separately and lawfully agreed, the dataset must not be used for:

- employee performance scoring,
- productivity surveillance,
- emotion, personality or health inference,
- biometric identification,
- participant re-identification,
- disciplinary or employment decisions,
- training outside the documented task and rights class,
- public redistribution of raw participant data,
- safety certification of a robotic system.

## 5. Task definition

### Instruction

> Pick up the cable, route it through guide one and guide two, align the connector, insert it fully and verify that it is seated.

### Success condition

A successful episode ends when:

- the cable passes through both guides in the required order,
- the connector orientation is correct,
- insertion reaches the defined seated state,
- the final state is visible and verified.

### Failure classes

- `missed_grasp`
- `cable_outside_guide`
- `excessive_slack`
- `connector_misaligned`
- `partial_insertion`
- `wrong_orientation`
- `verification_failed`
- `unknown_failure`

## 6. Composition

| Measure | Value |
|---|---:|
| Recorded episodes | [ ] |
| Accepted episodes | [ ] |
| Conditional episodes | [ ] |
| Rejected episodes | [ ] |
| Standard successes | [ ] |
| Variation successes | [ ] |
| Intentional failures | [ ] |
| Recovery episodes | [ ] |
| Participants | [ ] |
| Object variants | [ ] |
| Start-position variants | [ ] |
| Total video duration | [ ] |

## 7. Participants and collection context

Describe:

- participant recruitment and eligibility,
- whether participants were employees, contractors, founders or volunteers,
- compensation or paid demonstration time,
- voluntariness safeguards,
- age threshold,
- relevant skill or task familiarity,
- collection location,
- whether a works council or employer was involved,
- separation of identity records from delivered data.

Do not place names or direct identifiers in this public card.

## 8. Modalities

| Modality | Description |
|---|---|
| Camera 0 | [operator-side view, resolution, nominal FPS] |
| Camera 1 | [task-side view, resolution, nominal FPS] |
| Timestamps | [software monotonic clock / hardware clock] |
| Calibration | [intrinsics, distortion, extrinsics, target] |
| Task phases | [annotation procedure and format] |
| Failure/recovery | [taxonomy and annotation procedure] |
| Optional trajectories | [method, coordinate frame, uncertainty] |

## 9. Capture equipment

Document for each device:

- manufacturer and model,
- sensor type,
- lens and field of view if known,
- configured resolution,
- nominal frame rate,
- exposure and focus mode,
- mount and position,
- connection interface,
- timestamp method,
- firmware/driver environment when relevant.

## 10. Calibration

| Camera | Accepted frames | Mean reprojection error | Date | Calibration ID |
|---|---:|---:|---|---|
| camera_0 | [ ] | [ ] px | [ ] | [ ] |
| camera_1 | [ ] | [ ] px | [ ] | [ ] |

Describe the target, square/marker dimensions, coordinate convention and any known instability.

## 11. Variations

List all controlled factors and their values:

- cable start position,
- cable curvature/slack,
- connector orientation,
- guide position or spacing,
- object variant,
- participant,
- lighting condition,
- intentional failure state.

Attach or link the variation matrix. State which combinations were not captured.

## 12. Annotation process

Describe:

- annotator qualifications,
- annotation tool,
- phase definitions,
- failure/recovery definitions,
- quality-review process,
- independent second review if used,
- agreement or disagreement handling,
- annotation confidence field,
- corrections after customer review.

## 13. Quality results

| Metric | Result | Target | Status |
|---|---:|---:|---|
| Acceptance rate | [ ] | >= 90% | [ ] |
| Stream completeness | [ ] | 100% accepted episodes | [ ] |
| Timestamp integrity | [ ] | 100% accepted episodes | [ ] |
| Rights metadata coverage | [ ] | 100% | [ ] |
| Privacy review pass | [ ] | 100% delivered episodes | [ ] |
| Failure-class coverage | [ ] | [defined target] | [ ] |
| Recovery coverage | [ ] | >= 5 episodes in v0.1 | [ ] |

Summarize reject reasons and re-capture activity.

## 14. Timing and synchronization limitations

State:

- clock used for timestamps,
- whether cameras are hardware-triggered,
- observed start offset,
- median and p95 inter-frame intervals,
- missing-frame behavior,
- whether cross-view correspondence is approximate.

For the initial software-timestamped implementation, do not call the streams hardware-synchronized.

## 15. Rights, legal basis and provenance

For every delivered episode, record:

- rights class,
- participant-information version,
- relevant agreement version,
- collection date and location class,
- customer/project identifier where applicable,
- retention class,
- allowed recipients,
- permitted model-training scope,
- reuse permission,
- deletion obligations.

The data card should explain roles and controls but should not publish participant contracts or identity records.

## 16. Privacy and security controls

Document:

- audio disabled or reason audio was required,
- face-exclusion or redaction procedure,
- screen/name/document exclusion,
- encryption at rest and in transit,
- access roles,
- project separation,
- backup and restore controls,
- export logging,
- incident process,
- raw-data retention and deletion verification.

## 17. Known limitations and biases

Include at least:

- small sample size,
- limited participants,
- limited object and environment diversity,
- staged table-top task rather than normal production work,
- software timestamp limitations,
- possible annotation subjectivity,
- human-to-robot morphology and action mismatch,
- no demonstrated generalization to unseen robot hardware,
- no demonstrated safety or production performance.

## 18. Validation and benchmarks

State which checks were actually performed:

- schema validation,
- video decode test,
- calibration review,
- human annotation review,
- external robotics review,
- customer benchmark,
- model or policy before/after evaluation.

Do not list a benchmark as completed unless evidence exists.

## 19. Version history

| Version | Date | Change | Approved by |
|---|---|---|---|
| 0.1.0 | [ ] | Initial demonstrator release | [ ] |

## 20. Contact and issue reporting

Technical issues: [email / issue URL]  
Privacy requests: [email]  
Security incidents: [email / process]

## Approval

| Role | Name / ID | Date | Decision |
|---|---|---|---|
| Technical owner | [ ] | [ ] | [ ] |
| Quality reviewer | [ ] | [ ] | [ ] |
| Privacy/legal reviewer | [ ] | [ ] | [ ] |