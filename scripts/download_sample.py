
import csv
import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "sample" / "sample_register.csv"
OUTPUT = ROOT / "sample" / "source_files"
MANIFEST = OUTPUT / "download_manifest.json"

OUTPUT.mkdir(parents=True, exist_ok=True)

with REGISTER.open("r", encoding="utf-8-sig", newline="") as f:
    cases = list(csv.DictReader(f))

if len(cases) != 20:
    raise SystemExit(f"Expected 20 cases, found {len(cases)}")

manifest = []
failures = []

for case in cases:
    case_id = case["sample_id"].strip()
    repo = case["repository"].strip()
    commit = case["commit_hash"].strip()
    file_path = case["file_path"].strip()

    url = (
        f"https://raw.githubusercontent.com/{repo}/"
        f"{commit}/{quote(file_path, safe='/')}"
    )
    destination = OUTPUT / case_id / Path(file_path).name
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        request = Request(
            url,
            headers={"User-Agent": "CS4928-P13-Reproduction"}
        )
        with urlopen(request, timeout=30) as response:
            content = response.read()

        if not content:
            raise ValueError("Downloaded file is empty")

        destination.write_bytes(content)

        manifest.append({
            "sample_id": case_id,
            "repository": repo,
            "commit_hash": commit,
            "file_path": file_path,
            "build_system": case["build_system"].strip(),
            "source_url": url,
            "local_path": str(destination.relative_to(ROOT)),
            "size_bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "status": "downloaded",
        })
        print(f"OK {case_id}: {file_path}")

    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as exc:
        failures.append({"sample_id": case_id, "url": url, "error": str(exc)})
        print(f"FAILED {case_id}: {exc}")

MANIFEST.write_text(
    json.dumps(
        {"downloads": manifest, "failures": failures},
        indent=2
    ),
    encoding="utf-8"
)

print(f"\nDownloaded: {len(manifest)}/20")
print(f"Failed: {len(failures)}")
print(f"Manifest: {MANIFEST}")

if failures:
    raise SystemExit("Resolve download failures before running the detector.")
