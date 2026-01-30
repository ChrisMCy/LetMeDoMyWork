# Lessons Learned

This file contains important patterns and rules learned during development to help maintain consistency and avoid repeated mistakes.

## Factory Pattern Rules

### Factory Values Should Differ from Domain Defaults

**Rule**: When creating test data in Factory classes, always use values that are **different from the domain entity's default values**.

**Rationale**: This ensures that save & reload cycles in tests properly validate that values are being persisted and retrieved correctly. If factory values match defaults, tests might pass even when persistence logic is broken because the domain would fall back to defaults.

**When to Apply**: This rule applies to all test factories when adding new attributes with default values. For example, if a domain default is `True`, the factory should use `False`.
