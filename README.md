# CS4928 – Code Smells in Build Scripts

## Project Overview

This project investigates the occurrence and contextual impact of code smells in software build scripts. It is based on the research paper:

**Tamanna et al. (2025), *Your Build Scripts Stink: The State of Code Smells in Build Scripts*.**

The project uses the original `build-smell-sniffer` tool to investigate three selected build-smell categories in Maven and Gradle build files from public Java repositories.

The investigation focuses not only on whether the detector identifies potential smells, but also on whether those findings genuinely match the paper's definitions and represent problems in their surrounding build context.

## Research Questions

- **RQ1:** Can we reproduce the detection of code smells in build scripts identified in the original study in the Maven and Gradle files?
- **RQ2:** What are the effects of refactoring a detected build-script code smell on the build script and its associated behaviour?

## Selected Build Smells

The three smell categories are based on the definitions presented by Tamanna et al. (2025).

### 1. Insecure URLs

The paper defines Insecure URLs as the use of non-secure HTTP rather than HTTPS when fetching dependencies or uploading build artifacts. Such connections may expose communications to man-in-the-middle attacks or tampering.

- **Associated weakness:** CWE-319 – Cleartext Transmission of Sensitive Information.
- **Investigation:** HTTP URLs identified in build files are examined to establish their purpose and whether they represent an actual security concern.

### 2. Missing Dependency Version

This smell occurs when a dependency is declared without an explicit version number. The paper highlights that missing version information can lead to unstable or insecure dependency resolution.

- **Associated weakness:** CWE-440 – Expected Behavior Violation.
- **Investigation:** Dependency declarations without explicit versions are examined to determine whether their versions are supplied elsewhere, such as through parent POMs, dependency management, Gradle platforms or version catalogs.

### 3. Duplicates

The paper defines Duplicates as the redundant inclusion of the same dependency, code or configuration within a build script. This can increase maintenance overhead and potentially cause unexpected behaviour through overriding rules.

- **Associated weakness:** CWE-710 – Improper Adherence to Coding Standards.
- **Investigation:** Repeated dependencies and build-script elements are examined in context, considering differences in version, scope, configuration and purpose.

### Detection and Manual Auditing

The original Sniffer implementation is used to identify potential instances of the selected smells. Detector findings are not automatically considered confirmed smells or harmful vulnerabilities.

Manual auditing examines the source evidence, compares it against the selected definitions and considers the surrounding build-script context. This helps distinguish genuine findings from false positives and cases where a detected pattern does not demonstrate contextual harm.

## Reproduction Stages

### M2 – Initial Reproduction

The initial reproduction used a bounded sample of 20 eligible Maven and Gradle build files from 20 distinct Java repositories.

The sample consisted of:
- 12 Maven build files.
- 8 Gradle build files.

The selected files were recorded using stable sample IDs, repository names, commit hashes and file paths. Eligibility was reviewed before detector execution, and files with no detected smells were retained in the sample.

The original sample, detector outputs and manual-audit evidence are preserved as the baseline for subsequent work.

### Event A – Detector Evaluation

Event A investigated the behaviour of the selected detector rules in a newer software environment using held-out build files.

The purpose was to examine whether the original findings and known implementation limitations remained relevant under the changed environment. Event A is documented separately from the initial M2 reproduction.

### Extended Reproduction – 50-File Sample

Following Event A, the project scope was expanded to a target sample of 50 build files.

The original 20 M2 files will be retained, with 30 additional eligible files selected to extend the sample. This preserves consistency with the original reproduction and allows the initial results to be compared with the larger sample.

The extended reproduction will use the same three smell categories and preserve the original detector implementation. Additional findings and manual-audit results will be recorded as separate evidence alongside the original baseline.

The expanded sample is intended to provide a broader examination of the selected smells. However, it remains a bounded sample of Maven and Gradle files from Java projects rather than a reproduction of the paper's complete dataset.

## Repository Structure

```text
CS4928 - CODE SNIFFER/
│
├── audit/
│   ├── detector_results.csv
│   ├── detector_results.json
│   ├── detector_run_metadata.json
│   ├── manual_audit_*.csv
│   ├── Results Comparison.csv
│   └── correctionlog.md
│
├── JasonTesting/
│   └── Event A evidence
│
├── repos/
│
├── results/
│
├── sample/
│   ├── candidates.csv
│   ├── sample_register.csv
│   ├── samplemethod.md
│   ├── selected_smells.md
│   ├── eligbility_review.csv
│   └── source_files/
│
├── scripts/
│   ├── download_sample.py
│   └── run_detector.py
│
├── tests/
│
├── pull_and_lint.py
├── select_sample.py
└── README.md
```

## Running the Reproduction

The workflow is divided into separate stages:

1. Collect candidate Maven and Gradle build files from public Java repositories.
2. Select eligible files and record their repository revisions.
3. Download and preserve the selected build files.
4. Verify downloaded files using SHA-256 hashes.
5. Run the original Sniffer against the preserved files.
6. Manually audit detector findings against the selected smell definitions.

The relevant scripts are located in the `scripts/` directory and the sample-selection scripts are in the repository root.

**Note:** The detector repository path in `scripts/run_detector.py` is currently configured for the original development environment and may need to be adjusted on another machine.

## References

Tamanna, M., Chandrani, Y., Burrows, M., Wroblewski, B., Williams, L., and Wermke, D. (2025). *Your Build Scripts Stink: The State of Code Smells in Build Scripts*. Proceedings of the 40th IEEE/ACM International Conference on Automated Software Engineering (ASE 2025).

Original detector: [s3c2/build-smell-sniffer](https://github.com/s3c2/build-smell-sniffer).