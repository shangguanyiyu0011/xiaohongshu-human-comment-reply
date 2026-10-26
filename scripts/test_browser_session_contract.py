#!/usr/bin/env python3
"""Regression checks for the single-browser-session contract."""

from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"
REQUIRED = (
    "## 浏览器会话锁（强制）",
    "同一次任务只允许一个浏览器会话",
    "禁止在侧边栏浏览器和 Chrome/CDP 之间自动切换",
    "不得要求用户在第二个浏览器重复登录",
    "保持原会话并请求用户在原页面完成必要的手动一步",
    "用户明确要求更换浏览器",
    "如当前浏览器提供交接能力则按其文档交接",
)


def main() -> None:
    text = SKILL.read_text(encoding="utf-8")
    missing = [phrase for phrase in REQUIRED if phrase not in text]
    if missing:
        raise SystemExit("FAIL: missing browser-session rules: " + " | ".join(missing))
    print("PASS: single-browser-session contract is complete")


if __name__ == "__main__":
    main()
