# External Robotics Review

> Complete only after a qualified reviewer has actually reviewed the demonstrator. Do not pre-fill approval.

## Reviewer context

| Field | Value |
|---|---|
| Reviewer role | [ ] |
| Organization disclosed publicly? | [yes/no] |
| Relevant expertise | [ ] |
| Review date | [ ] |
| Materials reviewed | [ ] |
| Conflict of interest | [ ] |

## 1. Task relevance

- Is cable routing and connector insertion a useful first task for evaluating the proposed data-operations workflow?
- Which parts are representative of real robot-learning or integration problems?
- Which parts are too staged or simplified?

Findings: [ ]

## 2. Data modalities

Review whether the planned modalities are sufficient:

- multi-view RGB,
- RGB-D,
- object/hand trajectories,
- force/torque/tactile data,
- teleoperation,
- robot action-state logs,
- task phases,
- failure/recovery labels.

Which are mandatory for a useful customer test? [ ]

## 3. Camera and calibration design

- Are two camera views sufficient for the stated scope?
- Are key occlusions likely?
- Is the calibration procedure credible?
- Which coordinate frames must be defined?
- Should hardware synchronization be required before a customer pilot?

Findings: [ ]

## 4. Failure and recovery taxonomy

- Are the initial classes mutually understandable?
- Which failure states are missing?
- How should recovery success be defined?
- Should failure and recovery be separate episodes or continuous trajectories?

Findings: [ ]

## 5. Data schema and quality gates

- Is the episode schema technically useful?
- Are required fields missing?
- Are acceptance tests measurable?
- Which metrics would a real robotics team require?

Findings: [ ]

## 6. Human-to-robot transfer

- Which human actions can be represented object-centrically?
- Which actions cannot be transferred without robot morphology or action data?
- Would teleoperation or robot demonstrations be necessary?
- What evidence would distinguish useful human video from attractive but unusable footage?

Findings: [ ]

## 7. Benchmark recommendation

Propose one minimal technical benchmark:

```text
robot/model:
task:
baseline:
new data input:
evaluation set:
primary metric:
secondary metrics:
success threshold:
```

## 8. Major risks

Rank the three largest technical risks:

1. [ ]
2. [ ]
3. [ ]

## 9. Recommendation

- [ ] proceed to five equipment dry runs
- [ ] proceed to ten internal episodes
- [ ] redesign camera layout
- [ ] add depth
- [ ] add force/tactile data
- [ ] add teleoperation or robot actions
- [ ] change the first task
- [ ] not technically useful in current form

Rationale: [ ]

## 10. Changes made after review

| Recommendation | Accepted? | Change | Commit / evidence |
|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] |

## Public disclosure permission

- [ ] Reviewer permits publication of role only.
- [ ] Reviewer permits publication of name and organization.
- [ ] Reviewer does not permit public attribution.

Reviewer confirmation: [ ]
