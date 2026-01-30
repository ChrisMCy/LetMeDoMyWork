import json
import os
import sys
import time
from pathlib import Path

def detect_repo(file_path: str, project_dir: str) -> str:
    try:
        file_path_obj = Path(file_path).resolve()
    except Exception:
        file_path_obj = Path(file_path)

    try:
        project_dir_obj = Path(project_dir).resolve()
    except Exception:
        project_dir_obj = Path(project_dir)

    try:
        rel = file_path_obj.relative_to(project_dir_obj)
    except Exception:
        rel = file_path_obj

    parts = [p for p in rel.parts if p]
    if not parts:
        return "root"

    if len(parts) == 1:
        return "root"

    if parts[0].lower() == "reebuild":
        if len(parts) > 1 and parts[1].lower() in ("app", "worker", "scripts"):
            return f"{parts[0]}/{parts[1]}"
        return "reebuild"

    if parts[0].lower() in ("app", "worker", "scripts"):
        return parts[0]

    if parts[0].lower() in ("modules", "packages"):
        return f"reebuild/app/{parts[0]}"

    return parts[0]

def main():
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        data = json.loads(raw)
    except Exception:
        return

    tool_name = data.get("tool_name")
    if tool_name not in ("Edit", "MultiEdit", "Write"):
        return

    tool_input = data.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    if not file_path:
        return

    lower_path = file_path.lower()
    if lower_path.endswith(".md") or lower_path.endswith(".markdown"):
        return

    session_id = data.get("session_id") or "default"
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    cache_dir = Path(project_dir) / ".claude" / "tsc-cache" / session_id
    cache_dir.mkdir(parents=True, exist_ok=True)

    repo = detect_repo(file_path, project_dir)
    if not repo or repo == "unknown":
        return

    edited_log = cache_dir / "edited-files.log"
    with edited_log.open("a", encoding="utf-8") as f:
        f.write(f"{int(time.time())}:{file_path}:{repo}\n")

    affected_path = cache_dir / "affected-repos.txt"
    existing = set()
    if affected_path.exists():
        existing = {line.strip() for line in affected_path.read_text(encoding="utf-8").splitlines() if line.strip()}
    if repo not in existing:
        with affected_path.open("a", encoding="utf-8") as f:
            f.write(f"{repo}\n")

if __name__ == "__main__":
    main()
