# Physical AI Data Germany

[![Validate technical demonstrator](https://github.com/Aaron4815/Haallo/actions/workflows/demo-ci.yml/badge.svg)](https://github.com/Aaron4815/Haallo/actions/workflows/demo-ci.yml)
[![Test demonstrator end to end](https://github.com/Aaron4815/Haallo/actions/workflows/demo-integration-ci.yml/badge.svg)](https://github.com/Aaron4815/Haallo/actions/workflows/demo-integration-ci.yml)

**Public partner data room · Working title · Münster, Germany**

Physical AI Data Germany is an early-stage B2B venture building **task-specific, calibrated and legally documented training and validation data for robotics and Physical AI**.

- Public website: https://aaron4815.github.io/Haallo/
- Technical demonstrator: https://aaron4815.github.io/Haallo/demo.html
- Document and cooperation hub: https://aaron4815.github.io/Haallo/documents.html
- Structured collaboration intake: https://github.com/Aaron4815/Haallo/issues/new/choose

## What we are building

We do not sell generic video hours. We design and operate data campaigns for clearly defined robot tasks, including:

- synchronized or explicitly timestamped multi-view/RGB-D demonstrations,
- hand, tool and object trajectories where technically useful,
- systematic task and environment variation,
- failure and recovery sequences,
- annotation, quality assurance and acceptance criteria,
- rights, provenance, retention and deletion documentation,
- export to customer schemas or compatible robotics-data formats.

## Initial focus

Flexible industrial manipulation:

- cable routing and wire-harness operations,
- connector grasping, alignment and insertion,
- hoses, clips and deformable components,
- variable machine tending,
- inspection and corrective actions,
- failure and recovery behavior.

## Public technical proof

The repository now contains a v0.1 demonstrator for **cable routing and connector insertion**.

It includes:

- [demonstrator scope and evidence gates](demo/README.md),
- [capture protocol](demo/CAPTURE_PROTOCOL.md),
- [machine-readable episode schema](demo/episode.schema.json),
- [schema-valid example metadata](demo/example_episode.json),
- [acceptance tests](demo/ACCEPTANCE_TESTS.md),
- [data-card template](demo/DATA_CARD_TEMPLATE.md),
- [multi-view recorder](demo/record_multiview.py),
- [automated episode validator](demo/validate_episode.py),
- [quickstart guide](demo/QUICKSTART.md),
- automated schema and code validation,
- a green synthetic end-to-end integration test covering two-camera output, episode scaffolding and the full validator.

### Honest current boundary

This proves task definition, data architecture, documentation and initial software readiness. It does **not yet** prove:

- physical capture and calibration quality,
- industrial hardware synchronization,
- robot-policy improvement,
- transfer to unseen robot hardware,
- production safety,
- a secured technical co-founder,
- a paid production dataset.

The next evidence gate is physical capture: build the jig, calibrate two cameras, capture ten internal test episodes and publish measured quality results.

## Entry product

### 10-day Physical AI Feasibility Sprint

Planned introductory price for initial design partners: **EUR 4,900 net**.

Deliverables:

1. concrete task and modality specification,
2. controlled variation matrix,
3. data schema,
4. measurable acceptance criteria,
5. rights and provenance concept,
6. quality-assurance plan,
7. costed scope for a larger capture pilot,
8. final go/no-go workshop.

The sprint does not promise model improvement and does not automatically include a production dataset.

See: [PILOT_OFFER.md](PILOT_OFFER.md)

## We are looking for

### Design partners

Robot teams with:

- one concrete real-world task,
- a known or suspected data gap,
- a technical owner,
- an evaluation benchmark,
- willingness to scope a small paid feasibility engagement.

Open the structured form:  
https://github.com/Aaron4815/Haallo/issues/new?template=design-partner.yml

### System integrators and industrial partners

Partners with recurring customer cases where object variants, edge cases, failure states or site transfer generate additional engineering work.

### Technical Robotics / Data Lead

Senior practitioners in:

- computer vision,
- multi-view/RGB-D calibration,
- ROS 2,
- robot learning and imitation learning,
- teleoperation and action-state data,
- robotics data engineering,
- technical quality and privacy-by-design.

A paid four-week technical test is planned before any founder-level equity discussion.

Open the structured form:  
https://github.com/Aaron4815/Haallo/issues/new?template=technical-collaboration.yml

See: [TECHNICAL_COLLABORATION.md](TECHNICAL_COLLABORATION.md)

## Commercial model

1. Feasibility and task-design sprint
2. Capture pilot
3. Production data campaign
4. Recurring data operations
5. Later, carefully licensed reusable data assets

The market entry is project-based and evidence-gated. Hardware and hiring should follow qualified demand instead of speculative scale.

See: [BUSINESS_PLAN_EXECUTIVE_SUMMARY.md](BUSINESS_PLAN_EXECUTIVE_SUMMARY.md)

## Working principles

- no continuous or covert employee monitoring,
- voluntary, time-limited demonstration sessions,
- data minimization and no audio/face capture unless required,
- separate identity and dataset storage,
- project-specific rights and retention,
- no employee scoring, emotion recognition or hidden secondary use,
- documented customer acceptance and data provenance.

## Current stage

Completed or in progress:

- professional business plan and financial model,
- public partner website and document hub,
- feasibility-sprint offer,
- initial target-account pipeline and outreach,
- technical-lead role and test scorecard,
- public v0.1 technical demonstrator specification,
- recorder, validator, schema, structured intake forms and green automated CI.

Still required:

- physical demonstrator and measured calibration,
- first ten real internal episodes,
- external robotics review,
- first paid customer engagement,
- technical-lead contract or strong letter of intent,
- confirmed founder financing and availability,
- final legal, privacy and security package.

## Confidentiality and detailed documents

The full business plan, editable financial model, implementation tracker and personal/bank evidence are not published without context. They are available to qualified financing, research and cooperation partners after an initial discussion.

## Contact

**Aaron Wißmann**  
Münster, Germany  
Founder, Physical AI Data Germany — working title, in validation  
Email: **aaronwiss62@gmail.com**

For confidential tasks, use email rather than a public issue.
