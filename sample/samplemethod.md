# Sample Selection Method

## Original plan

The Week 5 sampling approach is recorded in the frozen assessment tracker. It will not be retrospectively rewritten.

## Executed sample

The assigned reproduction scope is 20 eligible Maven or Gradle build files from Java projects, subject to the applicable inclusion and exclusion criteria.

The candidate collection produced 112 build-file candidates from 56 unique repositories. The final sample contains 20 build files from 20 distinct repositories: 12 Maven files and 8 Gradle files.

## Selection procedure

Candidate repositories were collected using the GitHub search query `language:Java`, sorted by most recently updated repositories. The collection was limited to 100 repositories, a maximum of five build files per repository, and 300 candidates overall. Eligible file types were Maven `pom.xml` and Gradle `build.gradle` or `build.gradle.kts` files.

The selection script used SHA-256 hashing with the fixed seed `CS4928-P13-v1` to select one candidate file per repository and then select 20 repositories. This approach was chosen to reduce overrepresentation of repositories containing multiple build files.

The candidate list is recorded in `candidates.csv`, and the selected files are recorded in `sample_register.csv`.

## Case identification

Each selected build file has a stable case ID. The sample register records the repository URL, repository name, build-file path, build system, and commit SHA so that the selected files can be identified and retrieved at the recorded revisions.

## Inclusion of zero-detection files

All selected eligible files will remain in the sample, including files for which the detector reports no smells. Files will not be replaced or excluded based on detector results.

## Eligibility review

A teammate verified all 20 selected files against the eligibility criteria. All 20 were confirmed eligible and included in the sample. The review is recorded in `eligbility_review.csv`.

## Limitations and deviations

The executed selection procedure prioritised one build file per repository rather than simply taking the first 20 eligible files in a stable order. This was a deliberate choice to reduce the influence of repositories contributing multiple files, but it is a deviation that must be reported if the frozen Week 5 plan specified a different selection rule.

The candidate pool was limited to results returned by the GitHub search and was sorted by repository update date. It is therefore not a random sample of all Java projects. The sample is also limited to 20 Maven and Gradle build files from Java projects, so findings should not be generalised to all build systems or software projects.

Eligibility confirmation establishes that the files meet the inclusion criteria; it does not establish whether they contain code smells or whether any detected smells are harmful in context. These questions will be addressed separately during detection and manual auditing.

Any further discrepancies between the frozen plan and the executed procedure will be documented without retrospectively changing the original plan.