# Sample Collection Method

## Target sample
20 build scripts from public GitHub repositories, limited to Maven and Gradle.

## Selection procedure
1. Identify candidate Java repositories and their Maven or Gradle build files.
2. Record each candidate in `sample_register.csv`.
3. Check each candidate against the inclusion and exclusion criteria in the assigned paper and project pack.
4. Record the repository URL, exact commit hash, build-file path, build system, and inclusion decision.
5. Select 20 eligible build files for analysis, documenting any exclusions and the reason for each.
6. Preserve the original source and analyse disposable copies because the sniffer deletes files passed to it.

## Bias prevention
Do not select files based on whether the sniffer reports a smell. Apply the eligibility criteria before running the detector.

## Reproducibility
Record the collection date and exact revision of each selected file. Keep the sample register and any deviations under version control.

## Open item
Confirm the precise inclusion and exclusion criteria from the assigned paper and project pack before finalising the sample.
