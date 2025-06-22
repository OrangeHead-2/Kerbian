# KerbianCore Testing Module

KerbianCore's testing module provides a lightweight, extensible framework for:

- Unit testing
- Custom assertions
- Test discovery and execution
- Simple reporting

## Quickstart

```python
from kerbiancore.testing.core import test, TestRunner

@test
def test_addition():
    assert 1 + 2 == 3

runner = TestRunner()
runner.run_all()
```

## Features

- `@test` decorator for test functions
- `Assert` class for readable assertions
- Test suites and batch runners
- Integration with other KerbianCore modules

## More

- [Module API](./core.py)
- [Examples](./examples.py)
- [Tests](./tests.py)

---