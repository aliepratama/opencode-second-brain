"""Validate markdown files for common AI output artifacts.

Checks: Chinese characters, emoji in tables, backslash-n in Mermaid,
numbering in Mermaid nodes, special characters in Mermaid nodes.

Usage:
    python -m scripts .opencode/skills/para-md-validator path/to/file.md [--fix]
    python -m scripts .opencode/skills/para-md-validator daily/
"""

import os
import re
import sys
from pathlib import Path

CHINESE_RANGES = [
    (0x4E00, 0x9FFF),   # CJK Unified
    (0x3400, 0x4DBF),   # CJK Extended A
    (0xF900, 0xFAFF),   # CJK Compatibility
]

EMOJI_IN_TABLE_RE = re.compile(r"\|.*?[\U0001F300-\U0001F9FF].*?\|")
MERMAID_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
BACKSLASH_N_IN_NODE_RE = re.compile(r'"([^"]*?)\\n([^"]*?)"')
NUMBERING_IN_NODE_RE = re.compile(r'"[0-9]+[a-z]?\.\s')
SPECIAL_IN_NODE_RE = re.compile(r'"[^"]*?[&/%][^"]*?"')

KNOWN_CHINESE = {
    "依据": "based on",
    "设置": "setting",
    "信息": "information",
    "自动": "automatic",
    "数据": "data",
    "用户": "user",
    "系统": "system",
    "处理": "process",
    "文件": "file",
    "选择": "select",
    "确认": "confirm",
    "取消": "cancel",
    "保存": "save",
    "删除": "delete",
    "编辑": "edit",
    "搜索": "search",
    "登录": "login",
    "注册": "register",
    "配置": "configure",
    "位置": "location",
}


def _is_chinese(char: str) -> bool:
    cp = ord(char)
    return any(lo <= cp <= hi for lo, hi in CHINESE_RANGES)


def _find_chinese(text: str) -> list[tuple[int, str, str]]:
    results = []
    for i, line in enumerate(text.split("\n"), 1):
        for char in line:
            if _is_chinese(char):
                context = line.strip()[:60]
                suggestion = KNOWN_CHINESE.get(line.strip()[:4], "remove or translate")
                results.append((i, context[:60], suggestion))
                break
    return results


def _find_emoji_in_tables(text: str) -> list[tuple[int, str]]:
    results = []
    in_table = False
    for i, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("|") and "-" not in line.replace(" ", ""):
            in_table = True
        elif not line.strip().startswith("|"):
            in_table = False

        if in_table:
            if EMOJI_IN_TABLE_RE.search(line):
                results.append((i, line.strip()[:80]))
    return results


def _find_backslash_n_in_mermaid(text: str) -> list[tuple[int, str]]:
    results = []
    blocks = MERMAID_BLOCK_RE.finditer(text)
    for block in blocks:
        block_text = block.group(1)
        line_offset = text[:block.start()].count("\n") + 1
        for j, bline in enumerate(block_text.split("\n")):
            if BACKSLASH_N_IN_NODE_RE.search(bline):
                results.append((line_offset + j, bline.strip()[:80]))
    return results


def _find_numbering_in_mermaid(text: str) -> list[tuple[int, str]]:
    results = []
    blocks = MERMAID_BLOCK_RE.finditer(text)
    for block in blocks:
        block_text = block.group(1)
        line_offset = text[:block.start()].count("\n") + 1
        for j, bline in enumerate(block_text.split("\n")):
            if NUMBERING_IN_NODE_RE.search(bline):
                results.append((line_offset + j, bline.strip()[:80]))
    return results


def _find_special_in_mermaid(text: str) -> list[tuple[int, str]]:
    results = []
    blocks = MERMAID_BLOCK_RE.finditer(text)
    for block in blocks:
        block_text = block.group(1)
        line_offset = text[:block.start()].count("\n") + 1
        for j, bline in enumerate(block_text.split("\n")):
            if SPECIAL_IN_NODE_RE.search(bline):
                results.append((line_offset + j, bline.strip()[:80]))
    return results


def _fix_chinese(text: str) -> str:
    for cn, en in KNOWN_CHINESE.items():
        text = text.replace(cn, en)
    return text


def _fix_emoji(text: str) -> str:
    emoji_map = {"✅": "Done", "❌": "Not done", "🟠": "Warning", "🟡": "Pending",
                  "🟢": "Active", "🔴": "Critical", "⏳": "Waiting",
                  "🎯": "Focus", "🌀": "Scattered", "🌊": "Flow",
                  "😊": "Happy", "😐": "Neutral", "😫": "Tired"}
    for emoji, replacement in emoji_map.items():
        text = text.replace(emoji, replacement)
    return text


def _process_file(filepath: Path, fix: bool = False):
    text = filepath.read_text(encoding="utf-8")

    issues = {
        "chinese": _find_chinese(text),
        "emoji_tables": _find_emoji_in_tables(text),
        "backslash_n": _find_backslash_n_in_mermaid(text),
        "numbering": _find_numbering_in_mermaid(text),
        "special": _find_special_in_mermaid(text),
    }

    total = sum(len(v) for v in issues.values())
    if total == 0:
        return

    print(f"\n  File: {filepath.relative_to(filepath.parents[len(filepath.parents)-3])}")

    for category, findings in issues.items():
        if not findings:
            print(f"  [{category.replace('_', ' ').title()}]  OK")
            continue

        print(f"  [{category.replace('_', ' ').title()}]")
        if category == "chinese":
            for line, context, suggestion in findings:
                print(f"    Line {line}: Chinese char found → {suggestion}")
                print(f"      {context}")
        elif category == "emoji_tables":
            for line, context in findings:
                print(f"    Line {line}: Emoji in table cell → replace with text")
                print(f"      {context}")
        elif category == "backslash_n":
            for line, context in findings:
                print(f"    Line {line}: Backslash-n in Mermaid node → replace with ' - '")
                print(f"      {context}")
        elif category == "numbering":
            for line, context in findings:
                print(f"    Line {line}: Numbering at node start → 'Text - Regular'")
                print(f"      {context}")
        elif category == "special":
            for line, context in findings:
                print(f"    Line {line}: Special char (&/%/) in Mermaid → replace")
                print(f"      {context}")

    if fix and total > 0:
        text = _fix_chinese(text)
        text = _fix_emoji(text)
        filepath.write_text(text, encoding="utf-8")
        print(f"  [FIXED] Applied automatic fixes")

    return total


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python -m scripts <skill-dir> <file|folder> [--fix]")

    target = sys.argv[1]
    fix = "--fix" in sys.argv
    target_path = Path(target)

    if not target_path.exists():
        # Try relative to vault
        current = Path(os.getcwd())
        for parent in [current, *current.parents]:
            candidate = parent / target
            if candidate.exists():
                target_path = candidate
                break

    if not target_path.exists():
        raise SystemExit(f"ERROR: Path not found: {target}")

    print("=" * 60)
    print("  PARA Markdown Validator")
    print("=" * 60)

    total_issues = 0
    files_checked = 0

    if target_path.is_file() and target_path.suffix == ".md":
        issues = _process_file(target_path, fix) or 0
        total_issues += issues
        files_checked = 1
    elif target_path.is_dir():
        for f in sorted(target_path.glob("*.md")):
            if f.name == ".gitkeep":
                continue
            issues = _process_file(f, fix) or 0
            total_issues += issues
            files_checked += 1
    else:
        raise SystemExit(f"ERROR: Not a markdown file or directory: {target}")

    print()
    print("-" * 60)
    print(f"  Files checked: {files_checked}")
    print(f"  Issues found: {total_issues}")
    if total_issues > 0:
        print("  [FAIL] Fix issues before finalizing.")
        if not fix:
            print("  Run with --fix to auto-correct common issues.")


if __name__ == "__main__":
    main()
