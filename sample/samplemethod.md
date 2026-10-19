# Bounded Sample Collection Method — P13

## Target sample
20 build files in total from public Java projects using Maven or Gradle.

## Collection procedure
1. Search public GitHub repositories for supported build-file names:
   - Maven: `pom.xml`
   - Gradle: `build.gradle` and `build.gradle.kts`
2. Record eligible candidates and their repository, file path, source URL, and exact commit.
3. Apply the inclusion and exclusion criteria below before running the smell detector.
4. Remove duplicate entries.
5. Sort eligible candidates using a predefined, reproducible order: repository identifier, file path, then commit date where needed.
6. Select the first 20 eligible files in that order. If fewer than 20 eligible files can be found, use all eligible files and document the shortfall.
7. Freeze the selected sample identifiers before the main analysis.
8. Preserve the source files and run the detector only on disposable copies.

## Inclusion criteria
- The file is publicly accessible on GitHub.
- The repository is a Java project.
- The file is a Maven or Gradle build script.
- The file can be retrieved at a specific repository revision.

## Exclusion criteria
- Duplicate entries for the same build file and revision.
- Files that are not genuine Maven or Gradle build scripts.
- Files from projects that do not meet the Java-project requirement.
- Files whose source content cannot be retrieved.

## Important analysis rule
Do not exclude a selected file solely because the sniffer crashes, reports a parsing problem, or cannot analyse it successfully. Record the failure and assess its impact on the bounded reproduction instead.

## Reproducibility
Maintain the candidate and final sample records in `sample_register.csv`. Record the collection date, repository URL, commit hash, file path, inclusion decision, and any exclusions. Keep the selected sample and analysis evidence under version control.

## Relationship to the original study
The original paper collected build scripts using build-system filename searches and removed duplicates. This reproduction uses a narrower sample of 20 Maven/Gradle build files from Java projects, as required by the P13 project pack.
