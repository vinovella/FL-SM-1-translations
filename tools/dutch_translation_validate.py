#!/usr/bin/env python3
"""Validate Dutch Ren'Py translation files against embedded English source text.

The validator is intentionally standard-library only so it can run locally and in
GitHub Actions without installing project dependencies. It validates complete files,
not partially translated fragments.
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

TRANSLATE_RE = re.compile(r"^\s*translate\s+([A-Za-z_][\w]*)\s+([A-Za-z0-9_]+|strings)\s*:\s*$")
OLD_NEW_RE = re.compile(r'^\s*(old|new)\s+("(?:\\.|[^"\\])*")(?:\s*#.*)?\s*$')
TOKEN_RE = re.compile(
    r"\{[^{}]*\}|\[[^\[\]]+\]|%\([^)]+\)[#0 +\-]?(?:\d+|\*)?(?:\.\d+)?[diouxXeEfFgGcrs%]|"
    r"%[#0 +\-]?(?:\d+|\*)?(?:\.\d+)?[diouxXeEfFgGcrs%]|%%|\\[ntr]"
)
BRACE_TAG_RE = re.compile(r"\{([^{}]+)\}")


@dataclass(frozen=True)
class Unit:
    source: tuple[str, ...]
    target: tuple[str, ...]
    source_shape: str
    target_shape: str
    source_line: int
    target_line: int


@dataclass
class Block:
    language: str
    block_id: str
    line: int
    units: list[Unit] = field(default_factory=list)


@dataclass(frozen=True)
class Problem:
    path: str
    line: int
    code: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.code}: {self.message}"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def decode_literal(literal: str) -> str:
    try:
        value = ast.literal_eval(literal)
    except (SyntaxError, ValueError) as exc:
        raise ValueError(f"malformed quoted string: {exc}") from exc
    if not isinstance(value, str):
        raise ValueError("quoted value is not a string")
    return value


def extract_statement(line: str) -> tuple[tuple[str, ...], str] | None:
    """Return decoded visible strings and the non-translatable statement shape."""

    cursor = 0
    literals: list[str] = []
    shape_parts: list[str] = []

    while True:
        first = line.find('"', cursor)
        if first < 0:
            shape_parts.append(line[cursor:])
            break

        between = line[cursor:first]
        if literals and between and not between.isspace():
            raise ValueError("unexpected non-whitespace code between quoted string literals")
        shape_parts.append(between)

        escaped = False
        closing = None
        for index in range(first + 1, len(line)):
            char = line[index]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                closing = index
                break

        if closing is None:
            raise ValueError("missing closing quotation mark")

        literal = line[first : closing + 1]
        literals.append(decode_literal(literal))
        shape_parts.append('""')
        cursor = closing + 1

    if not literals:
        return None

    return tuple(literals), normalize_shape("".join(shape_parts))


def normalize_shape(value: str) -> str:
    return " ".join(value.strip().split())


def parse_translation_text(
    text: str,
    path_label: str = "<memory>",
    strict_missing_targets: bool = True,
) -> tuple[list[Block], list[Problem]]:
    lines = text.splitlines()
    blocks: list[Block] = []
    problems: list[Problem] = []
    current: Block | None = None
    index = 0

    while index < len(lines):
        line = lines[index]
        match = TRANSLATE_RE.match(line)
        if match:
            current = Block(language=match.group(1), block_id=match.group(2), line=index + 1)
            blocks.append(current)
            index += 1
            continue

        if current is None:
            index += 1
            continue

        if current.block_id == "strings":
            old_match = OLD_NEW_RE.match(line)
            if not old_match or old_match.group(1) != "old":
                index += 1
                continue

            source_line = index + 1
            try:
                source = decode_literal(old_match.group(2))
            except ValueError as exc:
                problems.append(Problem(path_label, source_line, "malformed-source-string", str(exc)))
                index += 1
                continue

            target_index = index + 1
            while target_index < len(lines) and not lines[target_index].strip():
                target_index += 1
            if target_index >= len(lines):
                if strict_missing_targets:
                    problems.append(Problem(path_label, source_line, "missing-target-string", "old string has no matching new string"))
                index += 1
                continue

            next_translate = TRANSLATE_RE.match(lines[target_index])
            target_match = OLD_NEW_RE.match(lines[target_index])
            if next_translate or not target_match or target_match.group(1) != "new":
                if strict_missing_targets:
                    problems.append(Problem(path_label, source_line, "missing-target-string", "old string is not followed by a new string"))
                index += 1
                continue

            try:
                target = decode_literal(target_match.group(2))
            except ValueError as exc:
                problems.append(Problem(path_label, target_index + 1, "malformed-target-string", str(exc)))
                index = target_index + 1
                continue

            current.units.append(Unit((source,), (target,), 'old ""', 'new ""', source_line, target_index + 1))
            index = target_index + 1
            continue

        stripped = line.lstrip()
        if not stripped.startswith("#"):
            index += 1
            continue

        commented = stripped[1:].lstrip()
        if '"' not in commented:
            index += 1
            continue

        try:
            source_statement = extract_statement(commented)
        except ValueError as exc:
            problems.append(Problem(path_label, index + 1, "malformed-source-string", str(exc)))
            index += 1
            continue
        if source_statement is None:
            index += 1
            continue

        target_index = index + 1
        while target_index < len(lines):
            candidate = lines[target_index]
            if TRANSLATE_RE.match(candidate):
                break
            if candidate.strip() and not candidate.lstrip().startswith("#"):
                break
            target_index += 1

        if target_index >= len(lines) or TRANSLATE_RE.match(lines[target_index]):
            if strict_missing_targets:
                problems.append(Problem(path_label, index + 1, "missing-target-string", "source comment has no translated statement"))
            index += 1
            continue

        try:
            target_statement = extract_statement(lines[target_index])
        except ValueError as exc:
            problems.append(Problem(path_label, target_index + 1, "malformed-target-string", str(exc)))
            index = target_index + 1
            continue
        if target_statement is None:
            if strict_missing_targets:
                problems.append(Problem(path_label, target_index + 1, "missing-target-string", "translated statement contains no quoted string"))
            index = target_index + 1
            continue

        source, source_shape = source_statement
        target, target_shape = target_statement
        current.units.append(Unit(source, target, source_shape, target_shape, index + 1, target_index + 1))
        index = target_index + 1

    return blocks, problems


def parse_translation_file(
    path: Path,
    strict_missing_targets: bool = True,
) -> tuple[list[Block], list[Problem]]:
    return parse_translation_text(
        path.read_text(encoding="utf-8-sig"),
        path.as_posix(),
        strict_missing_targets=strict_missing_targets,
    )


def token_counter(text: str) -> Counter[str]:
    return Counter(TOKEN_RE.findall(text))


def brace_tag_sequence(text: str) -> list[str]:
    return [match.group(0) for match in BRACE_TAG_RE.finditer(text)]


def validate_paired_tag_balance(source: str, target: str) -> str | None:
    source_tags = BRACE_TAG_RE.findall(source)
    paired_names = {
        tag[1:].split("=", 1)[0].strip()
        for tag in source_tags
        if tag.startswith("/")
    }
    if not paired_names:
        return None

    stack: list[str] = []
    for raw in BRACE_TAG_RE.findall(target):
        tag = raw.strip()
        name = tag.lstrip("/").split("=", 1)[0].strip()
        if name not in paired_names:
            continue
        if tag.startswith("/"):
            if not stack or stack[-1] != name:
                return f"closing tag {{{tag}}} does not match the current opening tag"
            stack.pop()
        else:
            stack.append(name)
    if stack:
        return "unclosed formatting tag(s): " + ", ".join(stack)
    return None


def load_allowlist(path: Path, glossary_path: Path) -> tuple[set[str], list[re.Pattern[str]], set[str]]:
    exact: set[str] = set()
    regexes: list[re.Pattern[str]] = []
    glossary_categories: set[str] = set()

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rule_type = (row.get("rule_type") or "").strip()
            value = row.get("value") or ""
            if rule_type == "exact":
                exact.add(value)
            elif rule_type == "glossary_category":
                glossary_categories.add(value)
            elif rule_type == "regex":
                if value == "^[[:space:][:punct:]]+$":
                    regexes.append(re.compile(r"^(?:\s|[^\w\s]|_)+$", re.UNICODE))
                else:
                    try:
                        regexes.append(re.compile(value))
                    except re.error as exc:
                        raise ValueError(f"invalid allowlist regex {value!r}: {exc}") from exc

    glossary_identical: set[str] = set()
    if glossary_categories:
        with glossary_path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                category = (row.get("category") or "").strip()
                source = row.get("source") or ""
                target = row.get("dutch") or ""
                if category in glossary_categories and source == target:
                    glossary_identical.add(source)

    return exact, regexes, glossary_identical


def is_identical_allowed(text: str, allowlist: tuple[set[str], list[re.Pattern[str]], set[str]]) -> bool:
    exact, regexes, glossary_identical = allowlist
    if text in exact or text in glossary_identical:
        return True
    return any(pattern.fullmatch(text) for pattern in regexes)


def block_map(blocks: list[Block]) -> dict[str, Block]:
    return {block.block_id: block for block in blocks}


def validate_target_file(
    target_path: Path,
    reference_path: Path,
    expected_language: str,
    allowlist: tuple[set[str], list[re.Pattern[str]], set[str]],
) -> list[Problem]:
    target_blocks, problems = parse_translation_file(target_path, strict_missing_targets=True)
    reference_blocks, reference_problems = parse_translation_file(reference_path, strict_missing_targets=False)
    for item in reference_problems:
        problems.append(Problem(target_path.as_posix(), item.line, "reference-parse-error", item.message))

    seen_ids: set[str] = set()
    for block in target_blocks:
        if block.language != expected_language:
            problems.append(Problem(target_path.as_posix(), block.line, "translation-key-mismatch", f"expected {expected_language!r}, found {block.language!r}"))
        if block.block_id in seen_ids and block.block_id != "strings":
            problems.append(Problem(target_path.as_posix(), block.line, "duplicate-block-id", f"duplicate translation block {block.block_id!r}"))
        seen_ids.add(block.block_id)

    target_ids = [block.block_id for block in target_blocks]
    reference_ids = [block.block_id for block in reference_blocks]
    if target_ids != reference_ids:
        problems.append(Problem(target_path.as_posix(), 1, "block-id-parity", "translation block identifiers/order differ from the reference file"))

    target_by_id = block_map(target_blocks)
    reference_by_id = block_map(reference_blocks)
    for block_id in reference_ids:
        target_block = target_by_id.get(block_id)
        reference_block = reference_by_id.get(block_id)
        if target_block is None or reference_block is None:
            continue
        if len(target_block.units) != len(reference_block.units):
            problems.append(Problem(target_path.as_posix(), target_block.line, "unit-count-parity", f"block {block_id!r} has {len(target_block.units)} units; expected {len(reference_block.units)}"))
            continue

        for unit_index, (target_unit, reference_unit) in enumerate(zip(target_block.units, reference_block.units), start=1):
            if target_unit.source != reference_unit.source:
                problems.append(Problem(target_path.as_posix(), target_unit.source_line, "source-text-modified", f"block {block_id!r} unit {unit_index} source text differs from reference"))
            if target_unit.source_shape != reference_unit.source_shape:
                problems.append(Problem(target_path.as_posix(), target_unit.source_line, "source-code-modified", f"block {block_id!r} unit {unit_index} source speaker/code shape differs from reference"))
            if block_id != "strings" and target_unit.source_shape != target_unit.target_shape:
                problems.append(Problem(target_path.as_posix(), target_unit.target_line, "speaker-or-code-modified", f"block {block_id!r} unit {unit_index} changed non-translatable code around the string"))

            if len(target_unit.source) != len(target_unit.target):
                problems.append(Problem(target_path.as_posix(), target_unit.target_line, "literal-count-parity", f"block {block_id!r} unit {unit_index} has a different number of visible string literals"))
                continue

            for literal_index, (source_text, target_text) in enumerate(zip(target_unit.source, target_unit.target), start=1):
                source_tokens = token_counter(source_text)
                target_tokens = token_counter(target_text)
                if source_tokens != target_tokens:
                    problems.append(Problem(target_path.as_posix(), target_unit.target_line, "token-parity", f"block {block_id!r} unit {unit_index} literal {literal_index} placeholder/tag/escape tokens differ from source"))

                if brace_tag_sequence(source_text) != brace_tag_sequence(target_text):
                    problems.append(Problem(target_path.as_posix(), target_unit.target_line, "format-tag-order", f"block {block_id!r} unit {unit_index} literal {literal_index} Ren'Py brace-tag sequence differs from source"))

                balance_error = validate_paired_tag_balance(source_text, target_text)
                if balance_error:
                    problems.append(Problem(target_path.as_posix(), target_unit.target_line, "format-tag-balance", f"block {block_id!r} unit {unit_index} literal {literal_index}: {balance_error}"))

                if source_text == target_text and not is_identical_allowed(source_text, allowlist):
                    problems.append(Problem(target_path.as_posix(), target_unit.target_line, "untranslated-identical", f"block {block_id!r} unit {unit_index} literal {literal_index} is still identical to English and is not allowlisted"))

    return problems


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def language_contract(config: dict) -> tuple[str, str, bool]:
    target = config["target_language"]
    key = target["renpy_language_key"]["proposed"]
    status = target["renpy_language_key"]["status"]
    root = key
    confirmed = status == "confirmed"
    return root, key, confirmed


def validate_repository(repo_root: Path, config: dict, allow_unconfirmed_contract: bool = False) -> list[Problem]:
    manifest_path = repo_root / config["inventory"]["manifest_path"]
    allowlist_path = repo_root / "docs/dutch/UNCHANGED_STRING_ALLOWLIST.csv"
    glossary_path = repo_root / "docs/dutch/DUTCH_GLOSSARY.csv"
    rows = load_manifest(manifest_path)
    allowlist = load_allowlist(allowlist_path, glossary_path)
    target_root_name, expected_language, confirmed = language_contract(config)
    target_root = repo_root / target_root_name

    problems: list[Problem] = []
    compiled = sorted(target_root.rglob("*.rpyc")) if target_root.exists() else []
    for path in compiled:
        problems.append(Problem(path.relative_to(repo_root).as_posix(), 1, "compiled-file-committed", "compiled .rpyc files must not be committed in the Dutch tree"))

    target_files = sorted(target_root.rglob("*.rpy")) if target_root.exists() else []
    if target_files and not confirmed and not allow_unconfirmed_contract:
        problems.append(Problem(target_root_name, 1, "language-contract-unconfirmed", "Dutch .rpy files exist while the Phase 0 Ren'Py language key is still unconfirmed"))
        return problems

    manifest_by_path = {row["relative_path"]: row for row in rows}
    for target_path in target_files:
        relative = target_path.relative_to(target_root).as_posix()
        row = manifest_by_path.get(relative)
        if row is None:
            problems.append(Problem(target_path.relative_to(repo_root).as_posix(), 1, "untracked-target-file", "target file is not present in the translation manifest"))
            continue
        reference_language = row["count_reference_language"]
        reference_path = repo_root / reference_language / relative
        if not reference_path.is_file():
            problems.append(Problem(target_path.relative_to(repo_root).as_posix(), 1, "missing-reference-file", f"reference file {reference_language}/{relative} does not exist"))
            continue
        problems.extend(validate_target_file(target_path, reference_path, expected_language, allowlist))

    return problems


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--config", type=Path, default=Path("docs/dutch/phase0-config.json"))
    parser.add_argument(
        "--allow-unconfirmed-contract",
        action="store_true",
        help="Validate target files using the proposed Phase 0 key even if maintainer confirmation is still pending",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    config_path = args.config if args.config.is_absolute() else repo_root / args.config
    config = load_json(config_path)
    problems = validate_repository(repo_root, config, args.allow_unconfirmed_contract)

    if problems:
        for problem in problems:
            print(problem.render(), file=sys.stderr)
        print(f"Dutch translation validation failed with {len(problems)} problem(s).", file=sys.stderr)
        return 1

    root, key, confirmed = language_contract(config)
    state = "confirmed" if confirmed else "proposed/unconfirmed"
    print(f"Dutch translation validation passed for root {root!r}, language key {key!r} ({state}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
