# Task 010: Create Directory Structure

## Phase
0 - Project Setup

## Description
Create the Clean Architecture folder structure for the project.

## Steps
Run the following commands from the project root:

```bash
cd lib

# Core
mkdir -p core/{constants,theme,utils,errors,di,navigation}

# Domain Layer
mkdir -p domain/{entities,repositories,usecases}

# Data Layer
mkdir -p data/{models,repositories,datasources}

# Presentation Layer
mkdir -p presentation/{screens,widgets,bloc}
mkdir -p presentation/screens/{main,todo,settings,statistics,onboarding}

# Services
mkdir -p services/{database,smtp,storage,background,notifications,network,lifecycle,email,backup}
```

## Expected Structure
```
lib/
├── core/
│   ├── constants/
│   ├── theme/
│   ├── utils/
│   ├── errors/
│   ├── di/
│   └── navigation/
├── data/
│   ├── models/
│   ├── repositories/
│   └── datasources/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
├── presentation/
│   ├── bloc/
│   ├── screens/
│   │   ├── main/
│   │   ├── todo/
│   │   ├── settings/
│   │   ├── statistics/
│   │   └── onboarding/
│   └── widgets/
├── services/
│   ├── database/
│   ├── smtp/
│   ├── storage/
│   ├── background/
│   ├── notifications/
│   ├── network/
│   ├── lifecycle/
│   ├── email/
│   └── backup/
└── main.dart
```

## Acceptance Criteria
- [ ] All directories created
- [ ] Structure matches Clean Architecture pattern
- [ ] No errors when running `flutter analyze`

## Dependencies
- Task 006 (Create Flutter Project)

## Parallel Work
Can run parallel with: Task 007, 008, 009

## Estimated Effort
10 minutes
