
# CS4928 Reproduction and Correction Log

## 1. Method Clarification — P13 Bounded Sample

The frozen workbook entry refers to keyword searches such as "code smell" and "dead code". On reviewing the paper's methodology, we distinguished its keyword-based search of GitHub issues from its filename-based collection of build scripts.

The bounded reproduction will use filename-based collection of Maven and Gradle build files from Java projects, consistent with the paper's build-script collection approach and the P13 requirement to analyse 20 build files.

The bounded sample remains limited to 20 eligible files. Candidate eligibility will be decided before running the detector, duplicates will be removed, and the selection order and exact file revisions will be recorded. The original frozen workbook entry is retained for traceability.

## 2. Detector Correction Log

### Purpose

The original detector will be preserved as the baseline. Potential implementation and reporting problems will be investigated, and any verified corrections will be analysed separately.

### C01 — Detector Exceptions and Smell Counts

- **Observation:** The detector wrapper may report an issue with a smell ID when a check raises an exception.
- **Investigation:** Verify whether these records are counted as detections.
- **Correction:** Separate failures from actual findings if the problem is confirmed.
- **Verification:** Record the test and before-and-after output.

### C02 — Multiple Checks Share a Smell Label

- **Observation:** Different checks may map to the same output label.
- **Investigation:** Compare the check logic with the original paper's definitions.
- **Correction:** Preserve the source check identifier and distinguish findings where justified.
- **Verification:** Record representative test cases and results.

### C03 — Maven Missing-Version Checks

- **Observation:** The active missing-version check may skip files with a parent POM.
- **Investigation:** Verify whether the dependency version is managed in the relevant configuration.
- **Correction:** Change the behaviour only if the investigation supports it.
- **Verification:** Record the relevant configuration and test results.

## 3. Results Policy

Original and corrected results will be stored separately. Every correction will include evidence, rationale, verification, and its impact on the findings. Unconfirmed issues will not be described as verified bugs.
