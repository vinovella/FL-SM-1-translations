#!/usr/bin/env python3
"""Generate the Dutch localization progress report from the Phase 0 manifest."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

STATUS_ORDER = ["not started", "in progress", "review", "done"]
PHASE_ORDER = ["Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6"]


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build_report(rows: list[dict[str, str]], config: dict, repo_root: Path) -> str:
    target_root = config["target_language"]["renpy_language_key"]["proposed"]
    target_dir = repo_root / target_root
    status_counts = Counter(row["status"] for row in rows)
    by_phase: dict[str, Counter[str]] = defaultdict(Counter)
    units_by_phase: dict[str, int] = defaultdict(int)
    words_by_phase: dict[str, int] = defaultdict(int)

    for row in rows:
        by_phase[row["phase"]][row["status"]] += 1
        units_by_phase[row["phase"]] += int(row["string_dialogue_count"])
        words_by_phase[row["phase"]] += int(row["source_word_estimate"])

    target_files = set()
    if target_dir.exists():
        target_files = {path.relative_to(target_dir).as_posix() for path in target_dir.rglob("*.rpy") if path.is_file()}

    manifest_paths = {row["relative_path"] for row in rows}
    tracked_target_files = len(target_files & manifest_paths)
    untracked_target_files = sorted(target_files - manifest_paths)
    done = status_counts["done"]
    total = len(rows)
    percent = (done / total * 100.0) if total else 0.0

    lines = [
        "# Dutch translation progress",
        "",
        "This file is generated from `docs/dutch/PHASE0_FILE_MANIFEST.csv`. Do not edit it manually.",
        "",
        f"- **Candidate files:** {total}",
        f"- **Done:** {done} ({percent:.1f}%)",
        f"- **In progress:** {status_counts['in progress']}",
        f"- **Review:** {status_counts['review']}",
        f"- **Not started:** {status_counts['not started']}",
        f"- **Tracked Dutch `.rpy` files present:** {tracked_target_files}",
        f"- **Untracked Dutch `.rpy` files present:** {len(untracked_target_files)}",
        f"- **Pinned upstream baseline:** `{config['source']['upstream_baseline_sha']}`",
        "",
        "## Progress by phase",
        "",
        "| Phase | Files | Not started | In progress | Review | Done | Source units | Source words |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for phase in PHASE_ORDER:
        counts = by_phase[phase]
        files = sum(counts.values())
        lines.append(
            f"| {phase} | {files} | {counts['not started']} | {counts['in progress']} | {counts['review']} | {counts['done']} | {units_by_phase[phase]} | {words_by_phase[phase]} |"
        )

    lines.extend(
        [
            "",
            "## Source-change detection",
            "",
            "`SOURCE_CONTENT_SNAPSHOT.csv` stores a per-file source fingerprint. Running `python tools/dutch_phase0_inventory.py --check` together with `python tools/dutch_source_snapshot.py --check` fails when candidate paths, source units, block identifiers or embedded English source text have changed without regenerating the tracking data.",
            "",
            "## Next work",
            "",
        ]
    )

    next_rows = [row for row in rows if row["status"] != "done"][:20]
    if next_rows:
        lines.extend(["| Phase | File | Status | Units | Words |", "| --- | --- | --- | ---: | ---: |"])
        for row in next_rows:
            lines.append(
                f"| {row['phase']} | `{row['relative_path']}` | {row['status']} | {row['string_dialogue_count']} | {row['source_word_estimate']} |"
            )
    else:
        lines.append("All manifest files are marked done.")

    if untracked_target_files:
        lines.extend(["", "## Untracked Dutch files", ""])
        for path in untracked_target_files:
            lines.append(f"- `{path}`")

    lines.append("")
    return "\n".join(lines)


def compare_or_write(path: Path, content: str, check: bool) -> bool:
    if check:
        existing = path.read_text(encoding="utf-8-sig") if path.exists() else None
        return existing == content
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="")
    return True


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--config", type=Path, default=Path("docs/dutch/phase0-config.json"))
    parser.add_argument("--output", type=Path, default=Path("docs/dutch/TRANSLATION_PROGRESS.md"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    config_path = args.config if args.config.is_absolute() else repo_root / args.config
    output_path = args.output if args.output.is_absolute() else repo_root / args.output
    config = load_config(config_path)
    rows = load_manifest(repo_root / config["inventory"]["manifest_path"])
    report = build_report(rows, config, repo_root)
    ok = compare_or_write(output_path, report, bool(args.check))
    if not ok:
        print(f"ERROR: {output_path} is stale; regenerate the progress report.", file=sys.stderr)
        return 1
    print(f"Dutch translation progress report OK: {len(rows)} candidate files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
