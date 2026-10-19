# Selected Build-Smell Definitions — P13

## Scope
This bounded reproduction analyses three selected build smells in 20 Maven/Gradle build files from public Java projects.

## 1. Insecure URLs

**Detection rule:** Flag build-script URLs that use `http://` rather than `https://`, following the original sniffer's detection behaviour.

**Manual audit:** Inspect each flagged URL and its purpose. Record whether it transmits sensitive information, downloads dependencies or other resources, redirects to HTTPS, or has another reason to require secure transport.

**Important distinction:** An HTTP URL is a detection, not automatic proof of a harmful vulnerability.

## 2. Missing Dependency Version

**Detection rule:** Flag dependency declarations that lack an explicit version, according to the original sniffer's Maven/Gradle checks.

**Manual audit:** Check whether the version is supplied elsewhere, such as through Maven dependency management, a parent POM, a Gradle platform, a version catalog, or another applicable mechanism. Record whether the dependency's version is actually unresolved.

**Important distinction:** A missing version in an individual declaration does not necessarily mean the dependency has no effective version.

## 3. Duplicate Dependencies

**Detection rule:** Flag repeated dependency declarations according to the original sniffer's implementation.

**Manual audit:** Check whether the declarations refer to the same dependency and whether differences in version, scope, configuration, or build context make the repetition intentional or problematic.

**Important distinction:** Repeated declarations are not automatically harmful; assess their actual effect in context.

## Recording results

For each detection, record:
- Sample ID and file path.
- Smell detected by the sniffer.
- Relevant source lines or declarations.
- Manual-audit decision: harmful, not harmful, or uncertain.
- Evidence and a brief justification.

Do not change the detector's rules after seeing results without recording the change. Preserve raw outputs and use disposable copies of source files because the sniffer may delete its input.

## Implementation verification

Before interpreting prevalence, inspect the original sniffer's checks for all three smells and record any limitations or differences between Maven and Gradle. The manual-audit criteria above are the intended interpretation rules, not a claim that the detector implements them perfectly.

## Verified Implementation Observations

Source inspected: original `s3c2/build-smell-sniffer` repository, commit `dfdb7b0597846730c7dd0bb85729f2a57e4fa0f3`.

### Insecure URLs
- Maven checks URL text and XML attributes, while Gradle scans source lines.
- Both flag URLs beginning with `http://`.
- The detector does not establish whether a particular URL creates a harmful security risk.

### Missing Dependency Version
- Maven defines `check_missing_dependency_versions` twice. Python uses the later definition.
- The later Maven check skips a dependency if it appears in dependency management or if the POM has any parent. The parent check may miss unresolved versions.
- Gradle has both parsed-dependency and raw-text checks. The raw-text check recognises only certain declaration formats, so other formats may be missed.

### Duplicate Dependencies
- Maven compares `groupId:artifactId`.
- Gradle compares `group:artifact`.
- Neither check distinguishes declarations by version or configuration before flagging a repeated identifier.

### Reproduction and audit rule
These observations describe the inspected implementation, not measured accuracy on the selected sample. Preserve the detector unchanged for the reproduction. Record its raw output, then manually inspect flagged cases and relevant context. Do not count a detector failure as proof that a smell is absent.
