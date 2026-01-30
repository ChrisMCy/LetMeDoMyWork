---
description: Execute the next pending task from dev/active with lowest number
argument-hint: Optional - specific task number to work on (e.g., "002"), otherwise picks lowest
---

You are a task execution specialist. Execute the next pending development task.

## Task Selection

1. **If $ARGUMENTS is provided**: Work on task with that number prefix
2. **Otherwise**: Find and work on the task file in `dev/active/` with the **lowest number prefix** (e.g., `001-...`, `002-...`)

## Task Discovery

Scan `dev/active/` directory for markdown files. **Each task has 3 files** with the same number prefix:
- `[NNN]-[phase]-[task-name].md` - Main task file (description, steps, acceptance criteria)
- `[NNN]-[phase]-[task-name]-context.md` - Implementation context and decisions
- `[NNN]-[phase]-[task-name]-tasks.md` - Checklist for tracking progress

**IMPORTANT:** All 3 files share the same `[NNN]-[phase]-[task-name]` prefix!

## Execution Workflow

### 1. Read and Understand the Task
- Read the main task file completely
- Read any companion files (`-context.md`, `-tasks.md`) if they exist
- Understand the acceptance criteria
- Check dependencies - ensure prerequisite tasks are in `dev/finished/`

### 2. Execute the Task
- Follow the steps outlined in the task file
- Run necessary commands, create files, make changes as required
- Test the work against acceptance criteria
- Document any issues or decisions made

### 3. Code Review (for code-related tasks)
**Skip this step for environment setup tasks (Phase 0).**

After writing code, spawn TWO agents using the Task tool:

**a) Architecture Review Agent:**
```
Use Task tool with subagent_type="general-purpose":
Prompt: "Review the code changes for this task against Clean Architecture principles and SOLID.
Check:
- Domain layer has no imports from data/presentation
- Dependencies point inward only
- Single Responsibility per class
- Interfaces used for dependencies
- No business logic in UI layer
Report any violations found."
```

**b) Refactor Planning Agent:**
```
Use Task tool with subagent_type="Plan":
Prompt: "Based on the code changes, identify any refactoring opportunities:
- Functions > 30 lines
- Classes > 200 lines
- Duplicate code
- Missing abstractions
- Code that violates SOLID
Create a brief refactor plan if issues found, otherwise confirm code is clean."
```

**Action on findings:**
- If violations found: Fix them before proceeding
- If refactoring needed: Either fix now or create follow-up task
- If clean: Proceed to step 4

### 4. Update Task Files
After completing the work:

**Update main task file**:
- Mark acceptance criteria checkboxes as complete: `- [x]`
- Add a "## Completion Notes" section with:
  - Summary of what was done
  - Any deviations from the original plan
  - Issues encountered and how they were resolved
  - Architecture review results (if applicable)
  - Last Updated: YYYY-MM-DD HH:MM

**Update/Create context file** (`dev/active/[task-name]-context.md`):
- Implementation state: COMPLETED
- Key decisions made
- Files modified and why
- Architecture review findings (if applicable)
- Any follow-up work needed
- Last Updated timestamp

**Update session context** (`dev/session-context.md`):
- Add entry about completed task
- Update "Last Updated" timestamp

### 5. Move to Finished
**Move ALL 3 task files** from `dev/active/` to `dev/finished/`:
- `[NNN]-[phase]-[task-name].md` - Main task file
- `[NNN]-[phase]-[task-name]-context.md` - Context file
- `[NNN]-[phase]-[task-name]-tasks.md` - Tasks checklist

Use glob pattern to catch all files with the task number prefix:
- Windows: `Move-Item -Path 'dev/active/NNN-*' -Destination 'dev/finished/'`
- Unix: `mv dev/active/NNN-* dev/finished/`

**IMPORTANT:** Verify all 3 files are moved before proceeding to git commit!

### 6. Git Commit
Create a git commit with the completed work:
```
git add .
git commit -m "Complete task [NNN]: [brief task description]

- [Summary of what was implemented]
- [Key files changed]
- Closes task [NNN]-[task-name]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

## Error Handling

- If task has unmet dependencies, report which tasks must be completed first
- If acceptance criteria cannot be met, document the blocker and ask for guidance
- If task requires manual user action (e.g., GUI installation), guide the user and wait for confirmation

## Output Summary

After completing, provide:
1. Task number and name that was completed
2. Brief summary of work done
3. Next task number available in `dev/active/`
4. Any blockers or follow-up items

## Notes
- Always verify work against acceptance criteria before marking complete
- Keep documentation concise but sufficient for future context
- If the task is environment setup that requires user intervention, provide clear instructions and confirm completion before proceeding
