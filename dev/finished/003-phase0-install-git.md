# Task 003: Install Git

## Phase
0 - Project Setup

## Description
Install Git version control system for source code management.

## Steps
1. Download Git:
   - Windows: https://git-scm.com/download/win
   - macOS: Pre-installed or `brew install git`
   - Linux: `sudo apt-get install git`
2. Run installer with default options
3. Configure Git identity:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## Acceptance Criteria
- [x] `git --version` shows Git 2.x or later (Git 2.50.1)
- [x] Git user name and email configured

## Completion Notes
- Git 2.50.1 already installed
- Updated git config: user.name="Moszinger", user.email="christian.mosz@gmail.com"
- Initialized git repo and connected to GitHub: https://github.com/ChrisMCy/LetMeDoMyWork
- Created .gitignore with Flutter/Android/IDE patterns
- Initial commit pushed to GitHub
- Note: Task 011 (Initialize Git Repo) also completed as part of this task
- Last Updated: 2026-01-30

## Dependencies
None

## Parallel Work
Can run parallel with: Task 002 (Install Android Studio)

## Estimated Effort
15 minutes
