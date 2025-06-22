# KerbianCore Security Module

Secure your app and codebase with KerbianCore's built-in security utilities.

## Features

- `SecureStore`: Encrypted key-value storage
- Code audit for secrets, insecure code, and vulnerabilities
- Utilities for managing and rotating secrets

## Example

```python
from kerbiancore.security.securestore import SecureStore

store = SecureStore("secrets.bin")
store.set("API_KEY", "s3cr3t")
assert store.get("API_KEY") == "s3cr3t"
```

---