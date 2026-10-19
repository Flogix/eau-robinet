"""01 — Download the national yearly zips (dis-YYYY.zip) listed by the data.gouv.fr API, with cache.

Idempotent and safe for data/raw/ (read-only by project rule):
  * a missing file is downloaded (to a .part file, renamed when its size and SHA1 match the API);
  * an existing file is never modified nor deleted: if it differs from the API (e.g. the current year
    was republished), the script reports it and stops, unless --update is passed, in which case the new
    version is saved next to it as dis-YYYY__<api-date>.zip.
Writes data/processed/source_manifest.json (file, size, SHA1, API date) for the app and the README.

Usage: python scripts/01_download.py [--update] [--no-hash]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402

PATTERN = re.compile(r"^dis-(\d{4})\.zip$")
HASH_CACHE = config.INTERIM / "sha1_cache.json"


def sha1_of(path: Path, cache: dict) -> str:
    """SHA1 of a file, cached by (size, mtime) so re-runs are instant."""
    st = path.stat()
    key = f"{path.name}|{st.st_size}|{st.st_mtime_ns}"
    if key not in cache:
        h = hashlib.sha1()
        with open(path, "rb") as f:
            while chunk := f.read(1 << 24):
                h.update(chunk)
        cache[key] = h.hexdigest()
    return cache[key]


def download(url: str, dest: Path, size: int, sha1: str) -> None:
    part = dest.with_suffix(dest.suffix + ".part")
    h = hashlib.sha1()
    with requests.get(url, stream=True, timeout=60) as r, open(part, "wb") as f:
        r.raise_for_status()
        for chunk in r.iter_content(1 << 20):
            f.write(chunk)
            h.update(chunk)
    if part.stat().st_size != size or h.hexdigest() != sha1:
        raise RuntimeError(f"{dest.name}: downloaded file does not match the API (size/SHA1) — kept as {part.name}")
    part.rename(dest)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="save newer API versions next to the local files")
    ap.add_argument("--no-hash", action="store_true", help="compare sizes only (faster)")
    args = ap.parse_args()

    config.RAW_DIS.mkdir(parents=True, exist_ok=True)
    config.INTERIM.mkdir(parents=True, exist_ok=True)
    cache = json.loads(HASH_CACHE.read_text()) if HASH_CACHE.exists() else {}

    meta = requests.get(config.DATASET_API, timeout=60).json()
    resources = sorted((r for r in meta["resources"] if PATTERN.match(r["title"])), key=lambda r: r["title"])
    manifest, problems = [], []
    for r in resources:
        name, size = r["title"], r["filesize"]
        api_sha1 = (r.get("checksum") or {}).get("value")
        dest = config.RAW_DIS / name
        if not dest.exists():
            print(f"[download] {name} ({size / 1e6:.0f} MB)")
            download(r["url"], dest, size, api_sha1)
            state = "downloaded"
        else:
            same = dest.stat().st_size == size and (args.no_hash or sha1_of(dest, cache) == api_sha1)
            if same:
                state = "up to date"
            elif args.update:
                new = dest.with_name(f"dis-{PATTERN.match(name).group(1)}__{r['last_modified'][:10]}.zip")
                if not new.exists():
                    print(f"[update] {name} differs from the API -> saving {new.name}")
                    download(r["url"], new, size, api_sha1)
                state = f"newer version saved as {new.name}"
            else:
                state = "DIFFERS FROM API"
                problems.append(name)
        print(f"{name:14s} {state}")
        manifest.append({"file": name, "size": size, "sha1": api_sha1, "api_last_modified": r["last_modified"],
                         "url": r["url"], "local_state": state})

    HASH_CACHE.write_text(json.dumps(cache, indent=1))
    config.PROCESSED.mkdir(parents=True, exist_ok=True)
    (config.PROCESSED / "source_manifest.json").write_text(json.dumps({
        "dataset_page": config.DATASET_PAGE, "dataset_last_update": meta.get("last_update"),
        "license": meta.get("license"), "files": manifest}, indent=1, ensure_ascii=False), encoding="utf-8")
    if problems:
        print(f"\n{len(problems)} local file(s) differ from the API: {problems}. Re-run with --update to fetch them.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
