
import csv
import hashlib
from collections import defaultdict
from pathlib import Path

candidates_path = Path("sample/candidates.csv")
register_path = Path("sample/sample_register.csv")
selection_notes_path = Path("sample/sample-selection-notes.txt")

with candidates_path.open(
    newline="", encoding="utf-8-sig"
) as handle:
    candidates = list(csv.DictReader(handle))

# Group eligible candidates by repository.
by_repository = defaultdict(list)

for row in candidates:
    if (
        row["repository"]
        and row["commit_hash"]
        and row["file_path"]
        and row["build_system"] in {"maven", "gradle"}
        and row["source_url"].startswith("https://github.com/")
    ):
        by_repository[row["repository"]].append(row)

# Choose one candidate per repository using a stable hash.
# This avoids selecting files based on detector results.
chosen = []

for repository, rows in by_repository.items():
    rows.sort(
        key=lambda row: (
            hashlib.sha256(
                f"CS4928-P13-v1|{row['repository']}|{row['file_path']}".encode()
            ).hexdigest(),
            row["file_path"].casefold(),
        )
    )
    chosen.append(rows[0])

# Apply a reproducible ordering to the repository selection.
chosen.sort(
    key=lambda row: hashlib.sha256(
        f"CS4928-P13-v1|{row['repository']}".encode()
    ).hexdigest()
)

chosen = chosen[:20]

if len(chosen) < 20:
    raise SystemExit(
        f"Only {len(chosen)} eligible repositories found; "
        "cannot create a 20-repository sample."
    )

fields = [
    "sample_id",
    "repository",
    "commit_hash",
    "file_path",
    "build_system",
    "source_url",
    "inclusion_decision",
    "exclusion_reason",
    "notes",
]

with register_path.open(
    "w", newline="", encoding="utf-8-sig"
) as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()

    for number, row in enumerate(chosen, start=1):
        writer.writerow({
            "sample_id": f"S{number:03d}",
            "repository": row["repository"],
            "commit_hash": row["commit_hash"],
            "file_path": row["file_path"],
            "build_system": row["build_system"],
            "source_url": row["source_url"],
            "inclusion_decision": "selected_pending_eligibility_review",
            "exclusion_reason": "",
            "notes": "Provisional selection; eligibility review required.",
        })

selection_notes_path.write_text(
    "CS4928 P13 provisional sample selection\n"
    "Candidate source: sample/candidates.csv\n"
    f"Candidate files: {len(candidates)}\n"
    f"Repositories with eligible-looking candidates: {len(by_repository)}\n"
    f"Selected files: {len(chosen)}\n"
    "Rule: retain one candidate per repository, selected using a "
    "SHA-256 hash of a fixed seed, repository name and file path; "
    "then select 20 repositories using a fixed-seed hash of the "
    "repository name.\n"
    "Seed: CS4928-P13-v1\n"
    "Detector results were not used in selection.\n"
    "Status: provisional. Review project eligibility and the "
    "Maven/Gradle balance before freezing the sample.\n",
    encoding="utf-8",
)

print(f"Created {register_path} with {len(chosen)} provisional files.")
print(f"Selected {len(set(r['repository'] for r in chosen))} unique repositories.")
print(f"Selection notes saved to {selection_notes_path}")
print("Review eligibility before running the detector.")
