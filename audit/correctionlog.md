# Method Clarification Log

## P13 bounded sample — build-script collection

The frozen workbook entry refers to keyword searches such as "code smell" and "dead code". On reviewing the paper's methodology, we distinguished its keyword-based search of GitHub issues from its filename-based collection of build scripts.

The bounded reproduction will use filename-based searches for Maven and Gradle build files, consistent with the paper's build-script collection approach and the P13 requirement to analyse 20 build files from Java projects.

The bounded sample remains limited to 20 eligible files. Candidate eligibility will be decided before running the detector, duplicates will be removed, and the selection order and exact file revisions will be recorded. The original frozen workbook entry is retained for traceability.
