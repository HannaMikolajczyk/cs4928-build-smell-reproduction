import os
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DETECTOR_DIR = Path(
    r"C:\Users\hmiko\Desktop\ORIGINAL CODE SNIFFER\build-smell-sniffer"
)
SOURCE_DIR = ROOT / "sample" / "source_files"
REGISTER = ROOT / "sample" / "sample_register.csv"
MANIFEST = SOURCE_DIR / "download_manifest.json"
OUTPUT_CSV = ROOT / "audit" / "detector_results.csv"
OUTPUT_JSON = ROOT / "audit" / "detector_results.json"
METADATA_JSON = ROOT / "audit" / "detector_run_metadata.json"

if not DETECTOR_DIR.is_dir():
    raise SystemExit(f"Detector repository not found: {DETECTOR_DIR}")

sys.path.insert(0, str(DETECTOR_DIR))
from secure_linter import lint_file_to_record

with REGISTER.open(encoding="utf-8-sig", newline="") as f:
    cases = list(csv.DictReader(f))

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
downloads = {
    item["sample_id"]: item
    for item in manifest["downloads"]
}

if len(cases) != 20:
    raise SystemExit(f"Expected 20 registered cases, found {len(cases)}")

if manifest["failures"]:
    raise SystemExit("Download failures exist; resolve them before analysis.")

detector_commit = subprocess.run(
    ["git", "rev-parse", "HEAD"],
    cwd=DETECTOR_DIR,
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()



results = []

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

fields = [
    "sample_id", "repository", "commit_hash", "file_path",
    "build_system", "source_sha256", "status", "smells",
    "error_type", "error_message",
]


def save_results():
    """Save progress after each sample so interrupted runs retain results."""
    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for item in results:
            record = item["detector_record"]
            writer.writerow({
                **{key: item.get(key) for key in fields if key in item},
                "smells": json.dumps(
                    record.get("smells", [])
                ) if record else "",
            })

    metadata = {
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "detector_directory": str(DETECTOR_DIR),
        "detector_commit": detector_commit,
        "sample_count": len(cases),
        "completed_runs": len(results),
        "successful_runs": sum(r["status"] == "OK" for r in results),
        "errors": sum(r["status"] == "ERROR" for r in results),
        "source_directory": str(SOURCE_DIR),
    }

    METADATA_JSON.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )


for case in cases:
    sample_id = case["sample_id"].strip()
    build_system = case["build_system"].strip().lower()
    download = downloads.get(sample_id)

    result = {
        "sample_id": sample_id,
        "repository": case["repository"].strip(),
        "commit_hash": case["commit_hash"].strip(),
        "file_path": case["file_path"].strip(),
        "build_system": build_system,
        "source_sha256": download.get("sha256") if download else None,
        "status": "ERROR",
        "detector_record": None,
        "error_type": None,
        "error_message": None,
    }

    try:
        if download is None:
            raise ValueError("No download manifest entry for this case.")

        source = ROOT / download["local_path"]

        if not source.is_file():
            raise FileNotFoundError(f"Preserved source file missing: {source}")

        actual_hash = hashlib.sha256(source.read_bytes()).hexdigest()
        if actual_hash != download["sha256"]:
            raise ValueError("Source SHA-256 does not match the download manifest.")

        suffix = "".join(Path(case["file_path"]).suffixes)
        with tempfile.NamedTemporaryFile(
            prefix=f"{sample_id}_",
            suffix=suffix,
            delete=False,
        ) as temp:
            temp_path = Path(temp.name)
            temp.write(source.read_bytes())

        try:
            record = lint_file_to_record(
                str(temp_path),
                explicit_build_system=build_system,
            )
            result["detector_record"] = record
            result["status"] = "OK"
        finally:
            temp_path.unlink(missing_ok=True)

    except Exception as exc:
        result["error_type"] = type(exc).__name__
        result["error_message"] = str(exc)

    results.append(result)
    save_results()

    record = result["detector_record"]
    smells = record.get("smells", []) if record else []
    print(f'{sample_id}: {result["status"]} - {smells or "(no recorded smells)"}')

print("\nRun summary")
print(f'Successful: {sum(r["status"] == "OK" for r in results)}/{len(cases)}')
print(f'Errors: {sum(r["status"] == "ERROR" for r in results)}/{len(cases)}')
print(f"CSV: {OUTPUT_CSV}")
print(f"JSON: {OUTPUT_JSON}")
print(f"Metadata: {METADATA_JSON}")
