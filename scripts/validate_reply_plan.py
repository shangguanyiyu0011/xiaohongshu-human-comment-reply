#!/usr/bin/env python3
"""Validate a Xiaohongshu comment-reply plan before any public send."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ALLOWED_ACTIONS = {"reply", "skip", "manual_review"}
REQUIRED_FIELDS = {
    "comment_id",
    "comment_text",
    "note_context",
    "existing_author_reply",
    "action",
    "reply",
    "reason",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def normalized(text: str) -> str:
    return "".join(str(text).lower().split()).strip("，。！？,.!?~～")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_reply_plan.py <plan.json>")

    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid UTF-8 JSON: {exc}")

    if not isinstance(data, list) or not data:
        fail("plan must be a non-empty JSON array")
    if len(data) > 10:
        fail("a batch may contain at most 10 items")

    seen_ids: set[str] = set()
    seen_replies: set[str] = set()
    reply_count = 0

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            fail(f"item {index} must be an object")
        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            fail(f"item {index} missing fields: {', '.join(sorted(missing))}")

        for field in REQUIRED_FIELDS - {"existing_author_reply"}:
            if not isinstance(item[field], str):
                fail(f"item {index} {field} must be a string")
        if not isinstance(item["existing_author_reply"], bool):
            fail(f"item {index} existing_author_reply must be a boolean")

        comment_id = str(item["comment_id"]).strip()
        comment_text = str(item["comment_text"]).strip()
        action = str(item["action"]).strip()
        reply = str(item["reply"]).strip()
        reason = str(item["reason"]).strip()

        if not comment_id or comment_id in seen_ids:
            fail(f"item {index} has an empty or duplicate comment_id")
        seen_ids.add(comment_id)
        if not comment_text or not reason:
            fail(f"item {index} needs comment_text and reason")
        if action not in ALLOWED_ACTIONS:
            fail(f"item {index} action must be one of {sorted(ALLOWED_ACTIONS)}")

        if action == "reply":
            reply_count += 1
            if item["existing_author_reply"] is not False:
                fail(f"item {index} cannot reply when an author reply already exists")
            if not str(item["note_context"]).strip():
                fail(f"item {index} needs note_context before replying")
            if not reply:
                fail(f"item {index} needs reply text")
            if len(reply) > 80:
                fail(f"item {index} reply exceeds 80 characters")
            key = normalized(reply)
            if not key or key in seen_replies:
                fail(f"item {index} has an empty or duplicate normalized reply")
            seen_replies.add(key)
        elif reply:
            fail(f"item {index} must leave reply empty for action={action}")

    print(f"OK: {len(data)} items validated; {reply_count} reply drafts passed mechanical checks (not sent)")


if __name__ == "__main__":
    main()
