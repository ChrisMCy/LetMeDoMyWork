# Reebuild Unit Test Writing Guidelines

## Framework

- `unittest.TestCase` (NO pytest)
- Files: `<UseCase>_test.py`
- Environment: `STAGE=local`

## Required setUp Pattern

```python
def setUp(self):
    factory_app = FactoryPostgresApplicationTestContainer.shared()
    injector = factory_app.get_injector(self)

    self.repo = injector.get(IRepository, self)
    self.uc = injector.get(UC < Name >)

    self.uc._service_dep = Mock()
    self.uc._uc_dep = Mock()
    self.uc.auth = Mock()

    self.entity = FactoryEntity.create_entity_full()
    self.repo.save(self.entity)
```

## Test Naming

**Pattern:** `test_<method>__<scenario>`

**Examples:**

- `test_execute__successful_operation`
- `test_execute__missing_entity_raises_exception`
- `test_execute__invalid_data_raises_value_error`

## Core Rules

| Rule            | Implementation                                                |
|-----------------|---------------------------------------------------------------|
| Repositories    | `factory_app.get_test_repo(IRepository, self)` - never mock   |
| UC Dependencies | Mock ALL: `self.uc._dependency = Mock()`                      |
| Test Data       | `FactoryEntity.create_entity_full()` - add methods if missing |
| Auth            | `self.uc.auth = Mock()` - never test auth()                   |
| Assertions      | `self.assertEqual()`, `self.assertRaises()` - NO bare assert  |
| Cleanup         | None needed - auto rollback                                   |

## Factory Usage

```python
# Single entity
self.entity = FactoryEntity.create_entity_full()
self.entity = FactoryEntity.create_entity_full(FactoryEntity.get_identifier_entity("code"))

# Multiple entities
entities = FactoryEntity.create_n_entity_full(5)
```

**If factory method missing:** Add it to the Factory class.

## Mock Configuration

```python
# Set return value
self.uc._service.execute.return_value = ServiceODTO(...)

# Verify calls
self.uc._service.execute.assert_called_once()

# Verify arguments
call_args = self.uc._service.execute.call_args[0][0]
self.assertEqual(call_args.field, expected_value)
```

## Common Test Patterns

**Success:**

```python
def test_execute__successful_operation(self):
    idto = UC < Name > IDTO(identifier=self.entity.identifier)
    odto = self.uc.execute(idto)
    self.assertEqual(odto.result, expected)
```

**Exception:**

```python
def test_execute__invalid_input_raises_value_error(self):
    idto = UC < Name > IDTO(field=None)
    with self.assertRaisesRegex(ValueError, "pattern"):
        self.uc.execute(idto)
```

**Not Found:**

```python
def test_execute__missing_entity_raises_exception(self):
    identifier = FactoryEntity.get_identifier_entity("nonexistent")
    idto = UC < Name > IDTO(identifier=identifier)
    with self.assertRaises(Exception):
        self.uc.execute(idto)
```
