# KerbianCore Security & Secure Storage Guide

## SecureStore Instructions

- Use `SecureStore` for secrets, config, and tokens.
- Store file is base64-encoded with permission checks.

```python
from kerbiancore.security.securestore import SecureStore, audit_secure_store

store = SecureStore("myapp.secrets")
store.set("db_password", "verysecret")
store.set("api_token", "token123")

print(store.get("api_token"))
print(audit_secure_store(store))
```

## Security Audit

- Use `audit_python_file` or `audit_module` to scan for bad patterns.

```python
from kerbiancore.security.audit import audit_python_file

issues = audit_python_file("my_module.py")
if issues:
    print("Security issues found:", issues)
```

---

- Always restrict permissions (0600) on your secret files.
- Never commit secrets to version control.

---