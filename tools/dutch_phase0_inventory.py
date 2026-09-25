#!/usr/bin/env python3
"""Generate the Phase 0 Dutch translation inventory from existing SM-1 language trees.

The candidate set is the union of editable .rpy paths across configured production
language roots. Counts are derived from the embedded English source comments/old
strings already present in Ren'Py translation files.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

TRANSLATE_RE = re.compile(r"^\s*translate\s+([A-Za-z_][\w]*)\s+([A-Za-z0-9_]+|strings)\s*:\s*$")
OLD_RE = re.compile(r"^\s*old\s+(?P<literal>\"(?:\\.|[^\"\\])*\")\s*$")
QUOTED_RE = re.compile(r'\"((?:\\.|[^\"\\])*)\"')
TOKEN_RE = re.compile(
    r"\{[^{}]*\}|\[[^\[\]]+\]|%\([^)]+\)[#0 +\-]?(?:\d+|\*)?(?:\.\d+)?[diouxXeEfFgGcrs%]|"
    r"%[#0 +\-]?(?:\d+|\*)?(?:\.\d+)?[diouxXeEfFgGcrs%]|%%"
)
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:['’\-][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*")

MANIFEST_FIELDS = [
    "relative_path",
    "phase",
    "status",
    "translation_block_count",
    "string_dialogue_count",
    "source_word_estimate",
    "count_reference_language",
    "present_in_languages",
    "structure_variance",
    "source_upstream_baseline_sha",
    "notes",
]


@dataclass(frozen=True)
class Metrics:
    language: str
    translation_blocks: int
    source_units: int
    source_words: int


def load_config(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_quoted_text(line: str) -> str | None:
    match = QUOTED_RE.search(line)
    return match.group(1) if match else None


def word_count(text: str) -> int:
    text = TOKEN_RE.sub(" ", text)
    text = text.replace(r"\n", " ").replace(r"\t", " ").replace(r"\r", " ")
    text = text.replace(r'\"', '"')
    return len(WORD_RE.findall(text))


def parse_translation_file(path: Path, language: str) -> Metrics:
    translation_blocks = 0
    source_units = 0
    source_words = 0
    current_block: str | None = None

    text = path.read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        translate_match = TRANSLATE_RE.match(line)
        if translate_match:
            translation_blocks += 1
            current_block = translate_match.group(2)
            continue

        if current_block is None:
            continue

        if current_block == "strings":
            old_match = OLD_RE.match(line)
            if old_match:
                source = extract_quoted_text(old_match.group("literal"))
                if source is not None:
                    source_units += 1
                    source_words += word_count(source)
            continue

        stripped = line.lstrip()
        if not stripped.startswith("#"):
            continue

        # Source-location comments such as '# game/code/foo.rpy:123' contain no
        # quoted dialogue and are naturally ignored here. Generated source-side
        # dialogue/menu comments do contain a quoted string.
        source = extract_quoted_text(stripped[1:])
        if source is not None:
            source_units += 1
            source_words += word_count(source)

    return Metrics(
        language=language,
        translation_blocks=translation_blocks,
        source_units=source_units,
        source_words=source_words,
    )


def discover_candidates(repo_root: Path, languages: list[str]) -> dict[str, list[str]]:
    candidates: dict[str, list[str]] = {}
    missing_roots: list[str] = []

    for language in languages:
        root = repo_root / language
        if not root.is_dir():
            missing_roots.append(language)
            continue
        for file_path in root.rglob("*.rpy"):
            if not file_path.is_file():
                continue
            relative = file_path.relative_to(root).as_posix()
            candidates.setdefault(relative, []).append(language)

    if missing_roots:
        raise RuntimeError(
            "Configured production language roots are missing: " + ", ".join(sorted(missing_roots))
        )
    return candidates


def phase_for_path(relative_path: str) -> str:
    if relative_path == "common.rpy":
        return "Phase 2"
    if relative_path == "code/hints.rpy":
        return "Phase 2"
    if relative_path.startswith(("code/renpy/", "code/classes/", "code/functions/", "code/debug/")):
        return "Phase 2"
    if relative_path.startswith(("code/data/", "code/live_chat/", "code/minigames/")):
        return "Phase 3"
    if relative_path.startswith("code/scenes/main_story/"):
        return "Phase 4"
    if relative_path.startswith(("code/scenes/character_scenes/", "code/scenes/cross_characters/")):
        return "Phase 5"
    if relative_path.startswith(("code/scenes/it_office/", "code/scenes/theatre/", "code/scenes/movies/")):
        return "Phase 6"
    return "Unassigned"


def load_existing_manual_fields(manifest_path: Path, allowed_statuses: set[str]) -> dict[str, tuple[str, str]]:
    if not manifest_path.exists():
        return {}

    result: dict[str, tuple[str, str]] = {}
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            path = (row.get("relative_path") or "").strip()
            status = (row.get("status") or "").strip()
            notes = row.get("notes") or ""
            if path and status in allowed_statuses:
                result[path] = (status, notes)
    return result


def choose_reference(
    repo_root: Path,
    relative_path: str,
    languages_present: list[str],
    preferred_order: list[str],
) -> tuple[Metrics, bool]:
    preference = {language: index for index, language in enumerate(preferred_order)}
    parsed = [
        parse_translation_file(repo_root / language / relative_path, language)
        for language in languages_present
    ]

    # Prefer the file exposing the greatest number of English source units, then
    # the greatest number of translation blocks and source words. Preference order
    # is only a tie-breaker.
    best = max(
        parsed,
        key=lambda item: (
            item.source_units,
            item.translation_blocks,
            item.source_words,
            -preference.get(item.language, len(preference)),
        ),
    )
    structures = {(item.translation_blocks, item.source_units) for item in parsed}
    return best, len(structures) > 1


def build_rows(repo_root: Path, config: dict) -> list[dict[str, str]]:
    languages = config["source"]["production_language_roots"]
    preferred = config["source"]["preferred_count_sources"]
    baseline = config["source"]["upstream_baseline_sha"]
    allowed_statuses = set(config["inventory"]["allowed_statuses"])
    default_status = config["inventory"]["default_status"]
    manifest_path = repo_root / config["inventory"]["manifest_path"]
    existing = load_existing_manual_fields(manifest_path, allowed_statuses)

    candidates = discover_candidates(repo_root, languages)
    rows: list[dict[str, str]] = []

    for relative_path in sorted(candidates):
        present = sorted(candidates[relative_path], key=lambda item: preferred.index(item) if item in preferred else 999)
        metrics, variance = choose_reference(repo_root, relative_path, present, preferred)
        status, notes = existing.get(relative_path, (default_status, ""))
        rows.append(
            {
                "relative_path": relative_path,
                "phase": phase_for_path(relative_path),
                "status": status,
                "translation_block_count": str(metrics.translation_blocks),
                "string_dialogue_count": str(metrics.source_units),
                "source_word_estimate": str(metrics.source_words),
                "count_reference_language": metrics.language,
                "present_in_languages": ";".join(present),
                "structure_variance": "yes" if variance else "no",
                "source_upstream_baseline_sha": baseline,
                "notes": notes,
            }
        )
    return rows


def render_manifest(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def render_summary(rows: list[dict[str, str]], config: dict) -> str:
    phases = ["Phase 2", "Phase 3", "Phase 4", "Phase 5", "Phase 6", "Unassigned"]
    totals: dict[str, dict[str, int]] = {
        phase: {"files": 0, "blocks": 0, "units": 0, "words": 0} for phase in phases
    }
    for row in rows:
        phase = row["phase"]
        totals.setdefault(phase, {"files": 0, "blocks": 0, "units": 0, "words": 0})
        totals[phase]["files"] += 1
        totals[phase]["blocks"] += int(row["translation_block_count"])
        totals[phase]["units"] += int(row["string_dialogue_count"])
        totals[phase]["words"] += int(row["source_word_estimate"])

    variance_count = sum(row["structure_variance"] == "yes" for row in rows)
    unassigned_count = totals.get("Unassigned", {}).get("files", 0)
    languages = ", ".join(f"`{item}`" for item in config["source"]["production_language_roots"])
    target = config["target_language"]
    storefront = config["storefront"]

    lines = [
        "# Phase 0 Dutch translation inventory summary",
        "",
        f"- **Upstream baseline:** `{config['source']['upstream_baseline_sha']}`",
        f"- **Candidate `.rpy` files:** {len(rows)}",
        f"- **Structural-variance files:** {variance_count}",
        f"- **Unassigned files:** {unassigned_count}",
        f"- **Production language roots used for union:** {languages}",
        "",
        "## Inventory by implementation phase",
        "",
        "| Phase | Files | Translation blocks | String/dialogue units | Source words (estimate) |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for phase in phases:
        values = totals.get(phase, {"files": 0, "blocks": 0, "units": 0, "words": 0})
        if phase == "Unassigned" and values["files"] == 0:
            continue
        lines.append(
            f"| {phase} | {values['files']} | {values['blocks']} | {values['units']} | {values['words']} |"
        )

    lines.extend(
        [
            "",
            "## Language-contract status",
            "",
            "| Decision | Proposed value | Status |",
            "| --- | --- | --- |",
            f"| Ren'Py key | `{target['renpy_language_key']['proposed']}` | `{target['renpy_language_key']['status']}` |",
            f"| Display name | `{target['display_name']['proposed']}` | `{target['display_name']['status']}` |",
            f"| Locale variant | `{target['locale_variant']}` | project target |",
            f"| Storefront metadata | `{storefront['proposed_filename']}` | `{storefront['status']}` |",
            "",
            "## Interpretation",
            "",
            "The candidate set is the union of editable `.rpy` paths across the configured production language roots. Generated `.rpyc` files are not candidates.",
            "",
            "Counts come from the available language copy that exposes the most embedded English source units for that path. `structure_variance=yes` means existing language trees disagree on block/unit counts and should receive extra attention during implementation; it does not remove the file from Dutch scope.",
            "",
            "Any `Unassigned` path is a Phase 0 failure and must be classified before Phase 0 can be closed.",
            "",
        ]
    )
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
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Fail when generated files differ from committed files")
    mode.add_argument("--write", action="store_true", help="Write generated manifest and summary (default)")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    config_path = args.config if args.config.is_absolute() else repo_root / args.config
    config = load_config(config_path)

    rows = build_rows(repo_root, config)
    manifest = render_manifest(rows)
    summary = render_summary(rows, config)

    manifest_path = repo_root / config["inventory"]["manifest_path"]
    summary_path = repo_root / config["inventory"]["summary_path"]
    check = bool(args.check)

    manifest_ok = compare_or_write(manifest_path, manifest, check)
    summary_ok = compare_or_write(summary_path, summary, check)

    unassigned = [row["relative_path"] for row in rows if row["phase"] == "Unassigned"]
    if unassigned:
        print("ERROR: Unassigned candidate paths:", file=sys.stderr)
        for path in unassigned:
            print(f"  - {path}", file=sys.stderr)
        return 2

    if check and not (manifest_ok and summary_ok):
        if not manifest_ok:
            print(f"ERROR: {manifest_path} is stale; regenerate the inventory.", file=sys.stderr)
        if not summary_ok:
            print(f"ERROR: {summary_path} is stale; regenerate the inventory.", file=sys.stderr)
        return 1

    print(
        f"Phase 0 inventory OK: {len(rows)} candidate .rpy files, "
        f"{sum(row['structure_variance'] == 'yes' for row in rows)} with structural variance, "
        "0 unassigned."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
