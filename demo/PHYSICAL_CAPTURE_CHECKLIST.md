# Physical Capture Execution Checklist

## Gate 0 — Do not start participant capture until complete

- [ ] task instruction frozen
- [ ] physical jig stable and photographed without people
- [ ] cable and connector variants identified
- [ ] both camera views tested
- [ ] audio disabled
- [ ] face, screens, documents and names outside framing
- [ ] local encrypted storage available
- [ ] participant information and rights class defined
- [ ] raw-data retention period defined
- [ ] capture operator and quality reviewer assigned

## Gate 1 — Equipment dry run

Record five equipment-only or founder-only dry runs.

For each dry run:

- [ ] both MP4 files created
- [ ] both timestamp files created
- [ ] videos decode fully
- [ ] frame/timestamp counts checked
- [ ] full task and final state visible
- [ ] queue drops recorded
- [ ] read failures recorded
- [ ] camera movement checked
- [ ] privacy review complete

Exit criterion:

- zero corrupt files,
- zero missing streams,
- no privacy exposure,
- timing metrics reported,
- fixture or camera changes documented.

## Gate 2 — Calibration

- [ ] target type and dimensions recorded
- [ ] at least 15 diverse calibration views per camera
- [ ] accepted-frame count recorded
- [ ] intrinsics and distortion saved
- [ ] extrinsic procedure documented
- [ ] mean reprojection error reported
- [ ] calibration IDs inserted into episode metadata
- [ ] camera mounts marked against accidental movement

Exit criterion:

- target mean reprojection error ≤ 1.0 px, or limitation explicitly accepted for 2D-only use.

## Gate 3 — First ten internal episodes

Planned mix:

- [ ] 5 standard successes
- [ ] 2 variation successes
- [ ] 1 intentional failure
- [ ] 2 recovery episodes

For every episode:

- [ ] unique episode ID
- [ ] valid participant pseudonym
- [ ] object and start-position variants assigned
- [ ] instruction ID recorded
- [ ] capture complete
- [ ] immediate quality review
- [ ] schema-valid metadata
- [ ] task phases annotated
- [ ] outcome and failure classes reviewed
- [ ] rights class present
- [ ] reject reasons present when rejected

## Gate 4 — Quality report

Publish aggregate, non-personal results:

- [ ] total recorded
- [ ] accepted / conditional / rejected
- [ ] acceptance rate
- [ ] stream completeness
- [ ] timestamp integrity
- [ ] median and p95 frame interval per camera
- [ ] cross-camera start-offset distribution
- [ ] calibration results
- [ ] failure/recovery coverage
- [ ] reject-reason distribution
- [ ] known limitations
- [ ] re-capture list

## Gate 5 — External review

Ask at least one qualified robotics practitioner to review:

- [ ] task usefulness
- [ ] camera layout
- [ ] synchronization claim
- [ ] schema and coordinate conventions
- [ ] failure/recovery taxonomy
- [ ] likely customer data modalities
- [ ] human-to-robot transfer limitations
- [ ] whether teleoperation or robot action-state data is required

Record feedback and resulting changes. Do not claim external validation until the reviewer has explicitly completed it.
