import tempfile
import unittest
from pathlib import Path

from foresight_hil.evaluation.document_links import (
    find_local_markdown_link_issues,
    format_document_link_report,
)


class DocumentLinksTest(unittest.TestCase):
    def test_finds_missing_local_markdown_links_and_skips_external_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "target.md").write_text("# target\n", encoding="utf-8")
            (root / "docs" / "guide.md").write_text(
                "\n".join([
                    "[root target](../target.md)",
                    "[missing](../missing.md)",
                    "[external](https://example.com)",
                    "![local image](../image.png)",
                ]),
                encoding="utf-8",
            )
            (root / "image.png").write_bytes(b"png")

            report = find_local_markdown_link_issues(root)

        self.assertFalse(report.ok)
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].file, Path("docs/guide.md"))
        self.assertEqual(report.issues[0].target, "../missing.md")
        self.assertIn("missing local link target", report.issues[0].message)
        self.assertIn("[document-links] FAIL", format_document_link_report(report))


if __name__ == "__main__":
    unittest.main()
