import json
import os
import re
import sys
from pathlib import Path

def main():
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        data = json.loads(raw)
    except Exception:
        return

    prompt = (data.get("prompt") or "").lower()
    if not prompt:
        return

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    rules_path = Path(project_dir) / ".claude" / "skills" / "skill-rules.json"
    try:
        rules = json.loads(rules_path.read_text(encoding="utf-8"))
    except Exception:
        return

    matched = []
    for skill_name, cfg in (rules.get("skills") or {}).items():
        triggers = cfg.get("promptTriggers") or {}
        keywords = triggers.get("keywords") or []
        if any(kw.lower() in prompt for kw in keywords):
            matched.append((skill_name, cfg))
            continue
        intent_patterns = triggers.get("intentPatterns") or []
        for pattern in intent_patterns:
            try:
                if re.search(pattern, prompt, re.IGNORECASE):
                    matched.append((skill_name, cfg))
                    break
            except re.error:
                continue

    if not matched:
        return

    by_priority = {"critical": [], "high": [], "medium": [], "low": []}
    for skill_name, cfg in matched:
        priority = (cfg.get("priority") or "low").lower()
        if priority not in by_priority:
            priority = "low"
        by_priority[priority].append(skill_name)

    lines = []
    lines.append("========================================")
    lines.append("SKILL ACTIVATION CHECK")
    lines.append("========================================")
    lines.append("")

    if by_priority["critical"]:
        lines.append("CRITICAL SKILLS (REQUIRED):")
        for name in by_priority["critical"]:
            lines.append(f"  -> {name}")
        lines.append("")

    if by_priority["high"]:
        lines.append("RECOMMENDED SKILLS:")
        for name in by_priority["high"]:
            lines.append(f"  -> {name}")
        lines.append("")

    if by_priority["medium"]:
        lines.append("SUGGESTED SKILLS:")
        for name in by_priority["medium"]:
            lines.append(f"  -> {name}")
        lines.append("")

    if by_priority["low"]:
        lines.append("OPTIONAL SKILLS:")
        for name in by_priority["low"]:
            lines.append(f"  -> {name}")
        lines.append("")

    lines.append("ACTION: Use Skill tool BEFORE responding")
    lines.append("========================================")

    sys.stdout.write("\n".join(lines))

if __name__ == "__main__":
    main()
