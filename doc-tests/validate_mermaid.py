#!/usr/bin/env python3
"""Validate Mermaid blocks embedded in RST docs."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

DOCS_DIR_DEFAULT = Path("docs/source")

KNOWN_DIAGRAM_PREFIXES = (
    "graph ",
    "flowchart ",
    "sequenceDiagram",
    "classDiagram",
    "stateDiagram",
    "stateDiagram-v2",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
    "mindmap",
    "timeline",
    "gitGraph",
    "quadrantChart",
    "requirementDiagram",
    "xychart",
    "sankey",
    "packet",
    "block",
)


@dataclass
class MermaidBlock:
    path: Path
    start_line: int
    lines: list[str]

    @property
    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


def parse_mermaid_blocks(rst_path: Path) -> list[MermaidBlock]:
    lines = rst_path.read_text(encoding="utf-8").splitlines()
    blocks: list[MermaidBlock] = []
    i = 0

    while i < len(lines):
        current = lines[i]
        if current.strip() != ".. mermaid::":
            i += 1
            continue

        block_start = i + 1  # 1-based line number for the directive
        i += 1
        block_lines: list[str] = []

        while i < len(lines):
            candidate = lines[i]
            if not candidate.strip():
                block_lines.append("")
                i += 1
                continue

            if candidate.startswith("   "):
                block_lines.append(candidate[3:])
                i += 1
                continue

            break

        # Trim leading/trailing blank lines inside the directive body.
        while block_lines and not block_lines[0].strip():
            block_lines.pop(0)
        while block_lines and not block_lines[-1].strip():
            block_lines.pop()

        blocks.append(MermaidBlock(path=rst_path, start_line=block_start, lines=block_lines))

    return blocks


def check_balanced_delimiters(block: MermaidBlock) -> list[str]:
    pairs = {")": "(", "]": "[", "}": "{"}
    opening = set(pairs.values())
    closing = set(pairs.keys())

    issues: list[str] = []
    stack: list[tuple[str, int]] = []

    for offset, line in enumerate(block.lines):
        # Ignore inline comments.
        source = line.split("%%", 1)[0]
        for ch in source:
            if ch in opening:
                stack.append((ch, offset + 1))
            elif ch in closing:
                if not stack or stack[-1][0] != pairs[ch]:
                    issues.append(
                        f"{block.path}:{block.start_line + offset}: unmatched '{ch}'"
                    )
                else:
                    stack.pop()

    for ch, local_line in stack:
        issues.append(f"{block.path}:{block.start_line + local_line - 1}: unmatched '{ch}'")

    return issues


def validate_block_shape(block: MermaidBlock) -> list[str]:
    issues: list[str] = []
    if not block.lines:
        issues.append(f"{block.path}:{block.start_line}: empty mermaid block")
        return issues

    first = next((ln.strip() for ln in block.lines if ln.strip()), "")
    if not first:
        issues.append(f"{block.path}:{block.start_line}: empty mermaid block")
        return issues

    if not first.startswith(KNOWN_DIAGRAM_PREFIXES):
        issues.append(
            f"{block.path}:{block.start_line}: unknown mermaid diagram start '{first}'"
        )

    issues.extend(check_balanced_delimiters(block))
    return issues


def validate_with_mmdc(blocks: list[MermaidBlock], mmdc_path: str) -> list[str]:
    issues: list[str] = []
    with tempfile.TemporaryDirectory(prefix="mmdc-validate-") as tmp_dir:
        tmp = Path(tmp_dir)
        for idx, block in enumerate(blocks):
            inp = tmp / f"diagram-{idx}.mmd"
            out = tmp / f"diagram-{idx}.svg"
            inp.write_text(block.text, encoding="utf-8")
            proc = subprocess.run(
                [mmdc_path, "-i", str(inp), "-o", str(out)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            if proc.returncode != 0:
                stderr = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "mmdc failed"
                issues.append(
                    f"{block.path}:{block.start_line}: mmdc validation failed: {stderr}"
                )
    return issues


def discover_blocks(docs_dir: Path) -> list[MermaidBlock]:
    blocks: list[MermaidBlock] = []
    for rst_path in sorted(docs_dir.rglob("*.rst")):
        blocks.extend(parse_mermaid_blocks(rst_path))
    return blocks


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Mermaid blocks in RST docs")
    parser.add_argument("--docs-dir", type=Path, default=DOCS_DIR_DEFAULT)
    parser.add_argument(
        "--require-mmdc",
        action="store_true",
        help="fail if mermaid-cli (mmdc) is not installed",
    )
    parser.add_argument(
        "--use-mmdc-if-available",
        action="store_true",
        help="use mmdc if present, otherwise fall back to structural checks only",
    )
    args = parser.parse_args()

    if not args.docs_dir.exists():
        print(f"error: docs directory not found: {args.docs_dir}", file=sys.stderr)
        return 2

    blocks = discover_blocks(args.docs_dir)
    if not blocks:
        print("No mermaid blocks found.")
        return 0

    issues: list[str] = []
    for block in blocks:
        issues.extend(validate_block_shape(block))

    mmdc = shutil.which("mmdc")
    if args.require_mmdc and not mmdc:
        print("error: --require-mmdc was set but 'mmdc' is not installed", file=sys.stderr)
        return 2

    if mmdc and (args.require_mmdc or args.use_mmdc_if_available):
        issues.extend(validate_with_mmdc(blocks, mmdc))

    if issues:
        print("Mermaid validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"Validated {len(blocks)} mermaid block(s).")
    if not mmdc and (args.use_mmdc_if_available or args.require_mmdc):
        print("Note: mmdc not installed; structural validation only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
