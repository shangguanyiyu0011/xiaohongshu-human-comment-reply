"""Exercise the public CLI using synthetic records and isolated temporary files."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_reply_plan.py"


def record(index: int = 1) -> dict:
    return {
        "comment_id": f"demo-{index}",
        "comment_text": "A synthetic question",
        "note_context": "Synthetic note context",
        "existing_author_reply": False,
        "action": "reply",
        "reply": f"A contextual draft {index}",
        "reason": "Synthetic test fixture",
    }


class PlanValidationTests(unittest.TestCase):
    def invoke(self, value=None, *, raw: bytes | None = None):
        with tempfile.TemporaryDirectory(prefix="reply-plan-test-") as folder:
            path = Path(folder) / "plan.json"
            path.write_bytes(raw if raw is not None else json.dumps(value).encode("utf-8"))
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                capture_output=True, text=True, encoding="utf-8", timeout=10,
            )

    def rejected(self, value, message):
        result = self.invoke(value)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_documented_demo_passes(self):
        value = json.loads((ROOT / "examples" / "reply-plan.demo.json").read_text(encoding="utf-8"))
        result = self.invoke(value)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 items validated; 1 reply drafts", result.stdout)
        self.assertIn("not sent", result.stdout)

    def test_ten_distinct_drafts_pass(self):
        self.assertEqual(self.invoke([record(i) for i in range(10)]).returncode, 0)

    def test_eleven_items_are_rejected(self):
        self.rejected([record(i) for i in range(11)], "at most 10")

    def test_non_array_or_empty_plan_is_rejected(self):
        for value in ([], {}, None, "text"):
            with self.subTest(value=value):
                self.rejected(value, "non-empty JSON array")

    def test_non_object_record_is_rejected(self):
        self.rejected(["record"], "must be an object")

    def test_missing_fields_are_rejected(self):
        value = record()
        del value["note_context"]
        self.rejected([value], "missing fields: note_context")

    def test_non_string_fields_are_rejected(self):
        for field in record().keys() - {"existing_author_reply"}:
            value = record()
            value[field] = None
            with self.subTest(field=field):
                self.rejected([value], f"{field} must be a string")

    def test_non_boolean_author_status_is_rejected(self):
        for status in (0, 1, None, "false"):
            value = record()
            value["existing_author_reply"] = status
            with self.subTest(status=status):
                self.rejected([value], "must be a boolean")

    def test_existing_author_reply_prevents_new_reply(self):
        value = record()
        value["existing_author_reply"] = True
        self.rejected([value], "author reply already exists")

    def test_duplicate_comment_id_is_rejected(self):
        first, second = record(1), record(2)
        second["comment_id"] = "  demo-1  "
        self.rejected([first, second], "duplicate comment_id")

    def test_duplicate_normalized_drafts_are_rejected(self):
        first, second = record(1), record(2)
        first["reply"] = "Thank you!"
        second["reply"] = "  THANK  YOU~  "
        self.rejected([first, second], "duplicate normalized reply")

    def test_empty_required_text_is_rejected(self):
        for field, message in (
            ("comment_id", "empty or duplicate comment_id"),
            ("comment_text", "needs comment_text and reason"),
            ("reason", "needs comment_text and reason"),
            ("note_context", "needs note_context"),
            ("reply", "needs reply text"),
        ):
            value = record()
            value[field] = "   "
            with self.subTest(field=field):
                self.rejected([value], message)

    def test_reply_length_boundary(self):
        value = record()
        value["reply"] = "a" * 80
        self.assertEqual(self.invoke([value]).returncode, 0)
        value["reply"] += "a"
        self.rejected([value], "exceeds 80 characters")

    def test_skip_and_manual_review_require_empty_reply(self):
        for action in ("skip", "manual_review"):
            value = record()
            value["action"] = action
            with self.subTest(action=action):
                self.rejected([value], "must leave reply empty")
                value["reply"] = ""
                self.assertEqual(self.invoke([value]).returncode, 0)

    def test_unknown_action_is_rejected(self):
        value = record()
        value["action"] = "send_now"
        self.rejected([value], "action must be one of")

    def test_invalid_json_and_encoding_are_reported(self):
        for raw in (b"{", b"\xff\xfe"):
            with self.subTest(raw=raw):
                result = self.invoke(raw=raw)
                self.assertEqual(result.returncode, 1)
                self.assertIn("cannot read valid UTF-8 JSON", result.stdout)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
