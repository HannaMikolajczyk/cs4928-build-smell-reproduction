Both M2 and Event A used the build-smell-sniffer Findings were mapped by hand to the three smells: 
“Missing GAV for dependency” and missing-version lines to Missing Dependency Version; 
http:// strings in the lint output to Insecure URLs; 
repeated declarations to Duplicate (Code/Dependency). 
Each flagged instance was then reviewed manually with the same fields in both studies.

What Transfers from M2 to Event A:
Missing Dependency Version: it still fires on dependencies whose version is managed elsewhere, such as a Spring Boot parent, or BOM. These findings are false positives.
Insecure URLs: it still fires on the XML namespace and schema strings in the POM header. These are identifiers, not download links.
Duplicate (Code/Dependency): it still produces a finding that is harmless.

What didn't Transfer / New findings:
A different kind of Duplicate case: E05 was a dependencyManagement plus dependency pair, while M2’s were repeated boilerplate lines.

Potiental Issues:
As the sample size for manual testing was smaller than before (10 files in Event A versus 20 in M2), there is less evidence behind each conclusion. Other issues:
Event A files ahd no real URLs and only one Duplication instance
