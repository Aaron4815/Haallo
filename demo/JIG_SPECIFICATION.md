# Physical Jig Specification v0.1

## Purpose

The jig creates a repeatable table-top cable-routing and connector-insertion task for internal demonstrator capture. It is not an industrial fixture and is not intended for force, safety or production certification.

## Functional requirements

The jig must provide:

- a stable base that does not move during normal hand manipulation,
- two cable guides with measurable positions,
- a connector receiving interface with a visible seated state,
- at least three repeatable cable start positions,
- at least three repeatable connector orientations,
- the ability to create a documented partial-insertion state,
- camera-visible markers or reference features,
- no sharp edges, exposed conductors or powered electrical connection.

## Recommended low-cost construction

### Base

- rigid board approximately 60 × 40 cm,
- matte, non-reflective surface,
- four non-slip feet,
- printed coordinate grid or removable measurement tape.

### Cable guides

- two smooth guides or rings,
- internal opening large enough to avoid cable damage,
- guide positions adjustable or replaceable,
- each guide assigned a visible identifier: `guide_1`, `guide_2`.

### Connector station

- unpowered connector pair or mechanically equivalent test interface,
- stable receiving side fixed to the base,
- visible seated-state indicator such as a reference line or mechanical stop,
- no live voltage and no production part unless use is authorized.

### Start-position markers

Mark at least:

- `start_left_near`
- `start_center_medium`
- `start_right_far`

### Orientation markers

Mark at least:

- `orientation_0_deg`
- `orientation_90_deg`
- `orientation_180_deg`

## Initial geometry record

Before capture, record in millimetres:

```text
base_width
base_height
guide_1_x
guide_1_y
guide_1_height
guide_2_x
guide_2_y
guide_2_height
connector_x
connector_y
connector_height
```

Define the origin and axis direction in a diagram or photograph that contains no participant or confidential background.

## Planned task variants

| Variant ID | Cable start | Connector orientation | Guide spacing | Intended class |
|---|---|---|---|---|
| V01 | left_near | 0° | standard | standard success |
| V02 | center_medium | 90° | standard | variation success |
| V03 | right_far | 180° | standard | variation success |
| V04 | left_near | misaligned | standard | intentional failure |
| V05 | center_medium | partial insertion | standard | recovery |

Expand the matrix only after the baseline can be captured reliably.

## Camera visibility requirements

From the combined two views, reviewers must see:

- all start-position markers,
- both guides,
- the full cable routing path,
- connector orientation,
- receiving interface,
- insertion and seated-state indicator,
- participant hands without requiring the face.

## Safety and privacy checklist

- [ ] no electrical power connected
- [ ] no sharp, hot or moving machine components
- [ ] fixture stable on the table
- [ ] cable cannot snag dangerously
- [ ] background cleared of screens, documents and names
- [ ] audio disabled
- [ ] face outside normal framing
- [ ] emergency stop is simply release/withdraw hands and stop capture

## Cost discipline

Use existing cameras and common materials for the first test where possible. Do not purchase industrial sensors, motion-capture systems or a robot before the software workflow, customer need and technical review justify them.

## Evidence required before completion

- bill of materials with actual cost,
- top-view geometry diagram,
- two camera-layout images without people,
- calibration target dimensions,
- five dry-run episodes,
- documented changes after dry-run review.
