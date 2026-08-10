# Quality Report — Technical Demonstrator v0.1

> Publish measured values only. Do not replace missing evidence with estimates.

## 1. Release summary

| Field | Value |
|---|---|
| Dataset version | [ ] |
| Capture dates | [ ] |
| Capture block IDs | [ ] |
| Jig version | [ ] |
| Recorder commit | [ ] |
| Schema version | [ ] |
| Reviewer | [pseudonymous/public identifier] |

## 2. Episode disposition

| Metric | Result |
|---|---:|
| Episodes recorded | [ ] |
| Accepted | [ ] |
| Conditional | [ ] |
| Rejected | [ ] |
| Acceptance rate | [ ] |
| Re-captured | [ ] |

## 3. Episode-class coverage

| Class | Planned | Recorded | Accepted |
|---|---:|---:|---:|
| Standard success | [ ] | [ ] | [ ] |
| Variation success | [ ] | [ ] | [ ] |
| Intentional failure | [ ] | [ ] | [ ] |
| Recovery | [ ] | [ ] | [ ] |

## 4. Stream integrity

| Camera | Episodes with stream | Decode pass | Frame/timestamp exact match | Queue drops | Read failures |
|---|---:|---:|---:|---:|---:|
| camera_0 | [ ] | [ ] | [ ] | [ ] | [ ] |
| camera_1 | [ ] | [ ] | [ ] | [ ] | [ ] |

## 5. Timing metrics

| Camera | Nominal FPS | Median interval ms | p95 interval ms | Min interval ms | Max interval ms |
|---|---:|---:|---:|---:|---:|
| camera_0 | [ ] | [ ] | [ ] | [ ] | [ ] |
| camera_1 | [ ] | [ ] | [ ] | [ ] | [ ] |

Cross-camera software start offset:

| Statistic | Value ms |
|---|---:|
| Minimum | [ ] |
| Median | [ ] |
| p95 | [ ] |
| Maximum | [ ] |

State explicitly:

- cameras hardware-triggered: [yes/no]
- common hardware clock: [yes/no]
- timestamp method: [ ]

## 6. Calibration

| Camera | Target | Accepted frames | Mean reprojection error px | Calibration ID |
|---|---|---:|---:|---|
| camera_0 | [ ] | [ ] | [ ] | [ ] |
| camera_1 | [ ] | [ ] | [ ] | [ ] |

Extrinsic-calibration method and result: [ ]

Any camera movement after calibration: [ ]

## 7. Failure coverage

| Failure class | Recorded | Accepted | Recovery attempted | Recovery successful |
|---|---:|---:|---:|---:|
| missed_grasp | [ ] | [ ] | [ ] | [ ] |
| cable_outside_guide | [ ] | [ ] | [ ] | [ ] |
| excessive_slack | [ ] | [ ] | [ ] | [ ] |
| connector_misaligned | [ ] | [ ] | [ ] | [ ] |
| partial_insertion | [ ] | [ ] | [ ] | [ ] |
| wrong_orientation | [ ] | [ ] | [ ] | [ ] |
| verification_failed | [ ] | [ ] | [ ] | [ ] |
| unknown_failure | [ ] | [ ] | [ ] | [ ] |

## 8. Reject reasons

| Reject reason | Count | Corrective action |
|---|---:|---|
| missing_camera_stream | [ ] | [ ] |
| corrupt_video | [ ] | [ ] |
| timestamp_gap | [ ] | [ ] |
| task_out_of_frame | [ ] | [ ] |
| camera_moved | [ ] | [ ] |
| privacy_exposure | [ ] | [ ] |
| wrong_task_instruction | [ ] | [ ] |
| variation_metadata_wrong | [ ] | [ ] |
| outcome_not_visible | [ ] | [ ] |
| unsafe_or_unplanned_action | [ ] | [ ] |
| other | [ ] | [ ] |

## 9. Rights and privacy

| Metric | Result |
|---|---:|
| Episodes with valid rights class | [ ] / [ ] |
| Episodes passing visual privacy review | [ ] / [ ] |
| Identity records included in delivered package | must be 0 |
| Audio streams included | [ ] |
| Privacy incidents | [ ] |
| Deletion exceptions | [ ] |

Describe any incident and resolution without publishing personal information.

## 10. Manual visual review

Reviewer confirms:

- [ ] complete task visible across the views
- [ ] final outcome visible
- [ ] phase annotations plausible
- [ ] intentional failures match metadata
- [ ] recovery episodes begin from defined error states
- [ ] no names, screens, documents or unrelated confidential material visible
- [ ] face excluded or separately justified and processed

## 11. Known limitations

At minimum discuss:

- software timestamps and lack of hardware trigger,
- camera and lens limitations,
- small participant and object sample,
- table-top staged task,
- annotation subjectivity,
- human-to-robot morphology/action mismatch,
- missing force/tactile/robot-action data,
- no demonstrated model or policy improvement,
- no production-safety evidence.

## 12. Deviations from plan

| Planned item | Actual | Reason | Impact |
|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] |

## 13. External review

| Reviewer role | Review date | Scope | Main findings | Changes made |
|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] |

Do not name a reviewer publicly without permission.

## 14. Final decision

- [ ] publish as internal technical proof
- [ ] publish sample metadata only
- [ ] share with named design partner
- [ ] re-capture required
- [ ] redesign required

Decision rationale: [ ]

## 15. Approval

| Role | Identifier | Date | Decision |
|---|---|---|---|
| Technical owner | [ ] | [ ] | [ ] |
| Quality reviewer | [ ] | [ ] | [ ] |
| Privacy/legal reviewer | [ ] | [ ] | [ ] |
