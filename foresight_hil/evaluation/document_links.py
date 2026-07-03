"""Validation helpers for local links in Markdown documents."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".codex", ".pytest_cache", "__pycache__"}
EXTERNAL_SCHEMES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "app://",
)


@dataclass(frozen=True)
class DocumentLinkIssue:
    file: Path
    target: str
    message: str


@dataclass(frozen=True)
class DocumentLinkReport:
    root: Path
    documents_checked: int
    links_checked: int
    issues: tuple[DocumentLinkIssue, ...]

    @property
    def ok(self):
        return not self.issues


def _iter_markdown_files(root):
    root_path = Path(root)
    for path in sorted(root_path.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def _target_path(raw_target):
    target = raw_target.strip()
    if not target:
        return ""
    if target.startswith("<") and ">" in target:
        target = target[1:target.index(">")]
    else:
        target = target.split()[0]
    target = unquote(target)
    if "#" in target:
        target = target.split("#", 1)[0]
    return target


def _should_skip_target(raw_target):
    target = raw_target.strip()
    if not target or target.startswith("#"):
        return True
    lower = target.lower()
    return lower.startswith(EXTERNAL_SCHEMES)


def find_local_markdown_link_issues(root="."):
    """Return missing-target issues for explicit Markdown links under root."""
    root_path = Path(root).resolve()
    issues = []
    documents_checked = 0
    links_checked = 0

    for document in _iter_markdown_files(root_path):
        documents_checked += 1
        text = document.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw_target = match.group(1)
            if _should_skip_target(raw_target):
                continue
            target = _target_path(raw_target)
            if not target:
                continue
            links_checked += 1
            candidate = Path(target)
            if not candidate.is_absolute():
                candidate = document.parent / candidate
            if not candidate.exists():
                issues.append(DocumentLinkIssue(
                    file=document.relative_to(root_path),
                    target=raw_target,
                    message=f"missing local link target: {target}",
                ))

    return DocumentLinkReport(
        root=root_path,
        documents_checked=documents_checked,
        links_checked=links_checked,
        issues=tuple(issues),
    )


def format_document_link_report(report):
    status = "OK" if report.ok else "FAIL"
    lines = [
        f"[document-links] {status} documents={report.documents_checked} "
        f"links={report.links_checked} issues={len(report.issues)}",
        f"[document-links] root={report.root}",
    ]
    for issue in report.issues:
        lines.append(
            f"[issue] file={issue.file} target={issue.target} :: {issue.message}"
        )
    return "\n".join(lines)
