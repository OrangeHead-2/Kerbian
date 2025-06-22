# KerbianCore Ecosystem - Unit Test Guide

## What is tested?

- **Registry**: Register, list, and remove plugins.
- **Hub**: Add, list, run plugins.
- **Installer**: Install plugin from a local file.
- **Manager**: Unified run logic via hub or registry.

---

## Run the tests

1. Copy `tests.py` into your KerbianCore ecosystem directory.
2. Run:

```bash
python tests.py
```

- *Note*: The installer test for local files is best run using `pytest` (with a `tmp_path` fixture), or adapt to your system.

---

- If all assertions pass, you'll see `All tests passed.`
- For more complete coverage, add tests for remote plugin install, error handling, and edge cases.

---