
#!/usr/bin/env python3
"""Collect a balanced pool of Maven/Gradle build-file candidates."""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://api.github.com"

BUILD_NAMES = {"pom.xml", "build.gradle", "build.gradle.kts"}

SKIP_DIRS = {
    ".git", ".gradle", ".idea", "node_modules", "build", "target",
    "out", "dist", "third_party", "vendor", "generated",
}

FIELDS = [
    "candidate_id", "repository", "commit_hash", "file_path",
    "build_system", "source_url", "inclusion_decision",
    "exclusion_reason", "notes",
]


def github_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "CS4928-build-smell-reproduction",
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def search_repositories(max_repos):
    found = []
    page = 1
    per_page = min(100, max_repos)

    while len(found) < max_repos:
        params = urllib.parse.urlencode({
            "q": "language:Java",
            "sort": "updated",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        })

        data = github_get(f"{API}/search/repositories?{params}")
        items = data.get("items", [])

        if not items:
            break

        for item in items:
            found.append(item["full_name"])
            if len(found) >= max_repos:
                break

        if len(items) < per_page:
            break

        page += 1
        time.sleep(1)

    return sorted(set(found), key=str.casefold)


def clone_repository(name, repos_dir):
    destination = repos_dir / name.replace("/", "__")

    if destination.exists():
        return destination

    result = subprocess.run(
        [
            "git", "clone", "--depth", "1", "--quiet",
            f"https://github.com/{name}.git", str(destination),
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Clone failed: {name}: {result.stderr.strip()}",
              file=sys.stderr)
        return None

    return destination


def get_commit(repo_dir):
    result = subprocess.run(
        ["git", "-C", str(repo_dir), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()


def find_build_files(repo_dir):
    found = []

    for path in repo_dir.rglob("*"):
        relative = path.relative_to(repo_dir)

        if any(part.casefold() in SKIP_DIRS
               for part in relative.parts[:-1]):
            continue

        if path.is_file() and path.name in BUILD_NAMES:
            found.append(path)

    return sorted(
        found,
        key=lambda p: p.relative_to(repo_dir).as_posix().casefold(),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Collect Java Maven/Gradle build-file candidates."
    )
    parser.add_argument("--max-repos", type=int, default=100)
    parser.add_argument("--max-candidates", type=int, default=300)
    parser.add_argument("--max-per-repo", type=int, default=5)
    parser.add_argument("--repos-dir", default="repos")
    parser.add_argument("--out", default="sample/candidates.csv")
    args = parser.parse_args()

    if args.max_repos < 1 or args.max_candidates < 1:
        parser.error("Repository and candidate limits must be positive.")
    if args.max_per_repo < 1:
        parser.error("--max-per-repo must be at least 1")

    repos_dir = Path(args.repos_dir)
    output = Path(args.out)
    repos_dir.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)

    print("Searching GitHub for Java repositories...")
    print("The smell detector will NOT be run.")

    try:
        repositories = search_repositories(args.max_repos)
    except Exception as exc:
        print(f"GitHub search failed: {exc}", file=sys.stderr)
        print("If rate-limited, set GITHUB_TOKEN and retry.",
              file=sys.stderr)
        return 1

    rows = []

    for number, name in enumerate(repositories, start=1):
        print(f"[{number}/{len(repositories)}] {name}")

        repo = clone_repository(name, repos_dir)
        if repo is None:
            continue

        try:
            commit = get_commit(repo)
            repo_count = 0

            for file in find_build_files(repo):
                if repo_count >= args.max_per_repo:
                    break
                if len(rows) >= args.max_candidates:
                    break

                relative = file.relative_to(repo).as_posix()
                build_system = (
                    "maven" if file.name == "pom.xml" else "gradle"
                )
                encoded_path = urllib.parse.quote(relative, safe="/")
                source_url = (
                    f"https://github.com/{name}/blob/"
                    f"{commit}/{encoded_path}"
                )

                rows.append({
                    "candidate_id": "",
                    "repository": name,
                    "commit_hash": commit,
                    "file_path": relative,
                    "build_system": build_system,
                    "source_url": source_url,
                    "inclusion_decision": "pending",
                    "exclusion_reason": "",
                    "notes": "",
                })
                repo_count += 1

            if len(rows) >= args.max_candidates:
                print("Candidate limit reached.")
                break

        except Exception as exc:
            print(f"Could not inspect {name}: {exc}", file=sys.stderr)

    rows.sort(key=lambda row: (
        row["repository"].casefold(),
        row["file_path"].casefold(),
        row["commit_hash"],
    ))

    for number, row in enumerate(rows, start=1):
        row["candidate_id"] = f"C{number:04d}"

    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    notes = output.with_suffix(".collection-notes.txt")
    notes.write_text(
        "CS4928 candidate collection\n"
        f"UTC timestamp: {datetime.now(timezone.utc).isoformat()}\n"
        "GitHub query: language:Java\n"
        "Repository search ordering: updated descending\n"
        f"Maximum repositories requested: {args.max_repos}\n"
        f"Repositories returned: {len(repositories)}\n"
        f"Maximum candidates: {args.max_candidates}\n"
        f"Maximum candidates per repository: {args.max_per_repo}\n"
        f"Candidates recorded: {len(rows)}\n"
        "Build-file names: pom.xml, build.gradle, build.gradle.kts\n"
        "Detector executed: no\n"
        "Selection based on detector output: no\n"
        "Limitation: GitHub search is not an exhaustive or random sample. "
        "Screen candidates against the project eligibility criteria before "
        "freezing the final sample.\n",
        encoding="utf-8",
    )

    print(f"\nRecorded {len(rows)} candidates in {output}")
    print(f"Collection notes saved to {notes}")
    print("No detector was run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
