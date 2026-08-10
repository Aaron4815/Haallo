# Robotics Dataset Data Card Template

This template is intended for task-specific Physical AI datasets. It is a working specification and does not replace customer contracts, privacy notices or safety documentation.

## 1. Dataset identity

- **Dataset name:**
- **Dataset version:**
- **Dataset ID:**
- **Date range:**
- **Data controller / contractual role:**
- **Technical owner:**
- **Customer / project:**
- **Confidentiality class:**

## 2. Intended decision and use

- **Robot task:**
- **Problem the dataset is meant to address:**
- **Primary intended use:**
- **Evaluation benchmark:**
- **Minimum useful improvement or decision threshold:**
- **Explicitly excluded uses:**

The data card must describe a decision or experiment. “General AI training” is not a sufficient purpose.

## 3. Collection design

- **Collection environment:** staged workbench / laboratory / customer site / other
- **Collection protocol version:**
- **Number of sessions:**
- **Number of episodes:**
- **Number of participants:**
- **Participant skill classes:**
- **Capture modalities:**
- **Nominal frequencies and resolutions:**
- **Synchronization method:**
- **Calibration method:**
- **Task instructions:**

## 4. Variation coverage

| Dimension | Planned values | Delivered values | Coverage gaps |
|---|---|---|---|
| Object / component | | | |
| Start pose | | | |
| Environment | | | |
| Lighting | | | |
| Tool / fixture state | | | |
| Failure class | | | |
| Recovery strategy | | | |
| Participant skill | | | |

## 5. Outcomes

| Outcome | Count | Share | Notes |
|---|---:|---:|---|
| Success | | | |
| Failure | | | |
| Successful recovery | | | |
| Failed recovery | | | |
| Aborted | | | |

## 6. Annotation

- **Task phases:**
- **Events:**
- **Object and fixture states:**
- **Trajectory representation:**
- **Annotation tooling:**
- **Annotation guidelines version:**
- **Quality sample size:**
- **Inter-review agreement or adjudication process:**

## 7. Quality summary

| Metric | Contract threshold | Delivered result | Status |
|---|---:|---:|---|
| Mandatory-stream completeness | | | |
| Maximum synchronization offset | | | |
| Median reprojection error | | | |
| Annotation acceptance | | | |
| Rights/provenance completeness | 100% | | |
| Accepted-episode rate | | | |

### Rejection reasons

- Missing stream:
- Synchronization failure:
- Calibration invalid:
- Task incomplete:
- Outcome ambiguous:
- Prohibited personal/confidential content:
- Rights/provenance incomplete:
- Other:

## 8. Rights, privacy and provenance

- **Legal / contractual collection basis:**
- **Participant notice or consent version:**
- **Employer / site agreement:**
- **Permitted uses:**
- **Prohibited uses:**
- **Export class:**
- **Retention class:**
- **Raw-data deletion date or rule:**
- **Identity-data separation:**
- **Face or audio presence:**
- **Confidential-information review:**
- **Sub-processors / annotation parties:**
- **Geographic storage location:**

## 9. Security

- **Encryption at rest and in transit:**
- **Access-control model:**
- **Project separation:**
- **Export logging:**
- **Backup and restore:**
- **Incident contact:**

## 10. Known limitations

Describe limitations that could materially affect model training or evaluation, including:

- participant or environment imbalance,
- missing failure classes,
- camera occlusion,
- inaccurate or estimated trajectories,
- limited force/tactile information,
- human-to-robot embodiment gap,
- domain shift,
- rights or retention restrictions.

## 11. Recommended and prohibited interpretation

### Recommended

- use within the documented task and benchmark,
- combine with robot action-state data when required,
- maintain episode-level rights and QA filtering,
- report accepted/rejected subsets separately.

### Prohibited

- employee productivity scoring,
- emotion or personality inference,
- identity recognition,
- hidden secondary use,
- claims of broad model performance not supported by the benchmark.

## 12. Delivery contents

- [ ] Data files
- [ ] Episode metadata
- [ ] Calibration files
- [ ] Annotation guidelines
- [ ] QA report
- [ ] Rights/provenance matrix
- [ ] File manifest and checksums
- [ ] Known-limitations register
- [ ] Deletion / retention record

## 13. Approval

| Role | Name / ID | Date | Decision |
|---|---|---|---|
| Technical QA | | | |
| Rights / privacy review | | | |
| Project owner | | | |
| Customer acceptance | | | |
