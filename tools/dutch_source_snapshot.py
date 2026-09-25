#!/usr/bin/env python3
"""Generate fingerprints for the embedded English source represented by the manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import sys
from pathlib import Path
from typing import Iterable

MODULE_PATH = Path(__file__).resolve().with_name("dutch_translation_validate.py")
SPEC = importlib.util.spec_from_file_location("dutch_translation_validate", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)

FIELDS = [
    "relative_path",
    "reference_language",
    "translation_block_count",
    "string_dialogue_count",
    "source_fingerprint_sha256",
]


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def fingerprint_blocks(blocks) -> str:
    parts: list[str] = []
    for block in blocks:
        parts.append(f"BLOCK\0{block.block_id}\n")
        for unit in block.units:
            parts.append(f"SHAPE\0{unit.source_shape}\n")
            for literal in unit.source:
                parts.append(f"TEXT\0{literal}\n")
    return hashlib.sha256("".join(parts).encode("utf-8")).hexdigest()


def build_rows(repo_root: Path, manifest_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in manifest_rows:
        relative = row["relative_path"]
        language = row["count_reference_language"]
        reference = repo_root / language / relative
        if not reference.is_file():
            raise RuntimeError(f"missing reference file: {language}/{relative}")
        blocks, problems = VALIDATOR.parse_translation_file(reference, strict_missing_targets=False)
        if problems:
            rendered = "; ".join(item.render() for item in problems[:5])
            raise RuntimeError(f"cannot fingerprint {language}/{relative}: {rendered}")
        result.append(
            {
                "relative_path": relative,
                "reference_language": language,
                "translation_block_count": str(len(blocks)),
                "string_dialogue_count": str(sum(len(block.units) for block in blocks)),
                "source_fingerprint_sha256": fingerprint_blocks(blocks),
            }
        )
    return result


def render_csv(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


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
    parser.add_argument("--manifest", type=Path, default=Path("docs/dutch/PHASE0_FILE_MANIFEST.csv"))
    parser.add_argument("--output", type=Path, default=Path("docs/dutch/SOURCE_CONTENT_SNAPSHOT.csv"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else repo_root / args.manifest
    output_path = args.output if args.output.is_absolute() else repo_root / args.output
    try:
        rows = build_rows(repo_root, load_manifest(manifest_path))
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    content = render_csv(rows)
    if not compare_or_write(output_path, content, bool(args.check)):
        print(f"ERROR: {output_path} is stale; regenerate the source snapshot.", file=sys.stderr)
        return 1
    print(f"Dutch source snapshot OK: {len(rows)} files fingerprinted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
