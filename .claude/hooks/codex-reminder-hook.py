import json
import os
import re
import sys
from datetime import datetime

CONFIRM_PATTERNS = [
    r"\bconfirm\s*:\s*proceed\b",
    r"\bconfirm\s*:\s*bypass\b",
]

KEYWORD_PATTERNS = [
    r"\breview\b",
    r"\bplan\b",
    r"\brefactor\b",
    r"\bdocs?\b",
    r"\barchitecture\b",
]

AGENT_SUGGESTIONS = [
    "code-architecture-reviewer",
    "plan-reviewer",
    "documentation-architect",
    "refactor-planner",
]

COMMAND_SUGGESTIONS = [
    "/dev-docs",
    "/dev-docs-update",
]

SKILL_SUGGESTIONS = [
    "reebuild-backend-guidelines",
    "skill-developer",
]


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        data = json.loads(raw)
    except Exception:
        return

    prompt = (data.get("prompt") or "")
    lower_prompt = prompt.lower()

    confirmed = any(re.search(pat, lower_prompt) for pat in CONFIRM_PATTERNS)
    if not confirmed:
        output = {
            "decision": "block",
            "reason": (
                "Blocked by Codex reminder hook. Add 'CONFIRM: proceed' to your prompt to continue. "
                "Tip: include /dev-docs when starting multi-step work."
            ),
        }
        print(json.dumps(output))
        return

    extra = []
    extra.append("CODex Reminder: Apply Reebuild rules and consider specialized agents/commands when relevant.")
    extra.append("Available agents: " + ", ".join(AGENT_SUGGESTIONS))
    extra.append("Available commands: " + ", ".join(COMMAND_SUGGESTIONS))
    extra.append("Relevant skills: " + ", ".join(SKILL_SUGGESTIONS))

    if any(re.search(pat, lower_prompt) for pat in KEYWORD_PATTERNS):
        extra.append("Keyword match detected; strongly consider the matching agent/command before proceeding.")

    context = "\n".join(extra)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
