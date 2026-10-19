# Initial Sniffer Smoke Test

## Environment
- Tool repository: s3c2/build-smell-sniffer
- Tool commit: dfdb7b0597846730c7dd0bb85729f2a57e4fa0f3
- Python: 3.12.2, selected through Poetry
- Test file: temporary Gradle file containing a Java plugin declaration

## Procedure
Created a disposable Gradle file in the Windows temporary directory and called `lint_file_to_record()` with `explicit_build_system="gradle"`.

## Observed result
- The detector ran and returned a record with `build_system: gradle`.
- The returned `smells` list was empty.
- The temporary input file did not exist after the call.

## Reproducibility and validity note
The detector deletes the file passed to it during analysis. Future tests must use disposable copies, not source sample files. This behaviour was confirmed experimentally in the smoke test.

## Limitation
This was a smoke test using one artificial file, not part of the research sample. It does not establish smell prevalence, detector accuracy, or reproduction of the original study's results.
