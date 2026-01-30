---
name: reebuild-backend-guidelines
description: Backend guidelines for Reebuild (Flask, GraphQL, Celery, DDD modules/packages). Use for use cases, repositories, GraphQL/REST, tasks, migrations, and testing.
---

# Reebuild Backend Guidelines

## Purpose

Provide consistent backend patterns for Reebuild's Python stack (Flask, GraphQL, Celery) using DDD modules and packages.

## When to Use This Skill

Use when working on:
- Use cases (UC* classes)
- Repositories (interfaces + SQL + in-memory)
- GraphQL queries/mutations and types
- Flask REST blueprints
- Celery tasks
- Domain entities, mappers, filters
- Database migrations and schema changes
- Tests under app/modules or app/packages

## Architecture Summary

### Module Layer (Application)

`app/modules/<feature>/`
- application/use_cases (UC* classes)
- application/tasks (Celery task classes)
- infrastructure/graphql (Query/Mutation + IG*/QG* types)
- infrastructure/rest (Flask blueprints)
- infrastructure/tasks (Tasks.py exports)
- configuration/injectors (DI providers)
- tests

### Package Layer (Domain + Persistence)

`app/packages/<pkg>/`
- domain/entities
- domain/filter_options
- application/repositories (interfaces)
- infrastructure/repositories/sql (models, mappers, repositories, filters)
- infrastructure/repositories/in_memory (repos, filters)
- tests/factories

## Critical Rules

- Data migrations: flag changes to defaults, mapper logic, enum values, field types, schema changes.
  Use: "Migration: <impact>".
- Repository pattern requires three layers updated together: Interface, SQL, InMemory.
- Tests must run from `reebuild/app` directory.
- Prefer existing utilities before adding helpers.
- No broad ruff operations across the whole project.
- Type hints use `T | None`, not Optional, and imports are module-level only.

## Use Case Pattern

- Naming: `UC<Noun><Verb>`
- Structure: IDTO/ODTO as dataclasses, constructor injected, `auth()` then `execute()`

Skeleton:

```
@dataclass
class UCNameIDTO(IUseCaseIDTO):
    ...

@dataclass
class UCNameODTO(IUseCaseODTO):
    ...

class UCName:
    @inject
    def __init__(self, repo: IRepository, ...):
        ...

    def auth(self, idto, **kwargs) -> None:
        ...

    def execute(self, idto) -> UCNameODTO:
        ...
```

## Repository Pattern

- Interface: `application/repositories/IRepository<Entity>.py`
- SQL: `infrastructure/repositories/sql/repositories/RepositorySql<Entity>.py`
- InMemory: `infrastructure/repositories/in_memory/RepositoryInMem<Entity>.py`
- Identical signatures across all layers.
- Prefer FilterOptions for dynamic filters.

## GraphQL and REST

- GraphQL: IG* inputs, QG* outputs, Query/Mutation classes in infrastructure/graphql.
- REST: blueprints in infrastructure/rest and registered in config/modules.py.
- Use custom scalars, not graphene.Int/Decimal.

## Celery

- Implement task classes in application/tasks.
- Export in infrastructure/tasks/Tasks.py using @instrumented_task.
- Delegate to get_task().

## Testing

- Framework: unittest.TestCase.
- Tests are near the code under modules/packages.
- Use factories in packages/tests/factories.

## Migration and Schema Work

- Alembic lives in `modules/main/main/database/alembic/`.
- Any schema or mapper changes require a migration warning.

## Utilities

- Prefer `reebuild_foundation/utils` and specialized helpers before adding new code.

## Related Files

- `CLAUDE.md` for project rules and architecture
- `AGENTS.md` for agent-level instructions
