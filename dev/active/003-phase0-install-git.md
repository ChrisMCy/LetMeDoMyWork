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
- [ ] `git --version` shows Git 2.x or later
- [ ] Git user name and email configured

## Dependencies
None

## Parallel Work
Can run parallel with: Task 002 (Install Android Studio)

## Estimated Effort
15 minutes
