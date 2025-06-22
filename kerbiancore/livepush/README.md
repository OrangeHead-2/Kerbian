# KerbianCore LivePush — Live Code Push Production Service

A secure, production-ready Python system for live code bundle updates, patching, and rollback.

---

## Features

- **Secure storage:** Bundle versioning, tamper-proof, rollback
- **Patch/delta support:** Only send diffs, not full bundles
- **Authentication & permissions:** Token-based, scope control
- **Atomic updates:** Download, verify, and swap in one step
- **Update hooks:** Pre/post update/rollback, error handling
- **Background checks:** Auto-update, staged rollout, A/B testing
- **Protocol:** Chunked, resumable, encrypted, signed transfer

---

## Server Example

```python
from kerbiancore.livepush.server import LivePushServer
server = LivePushServer("bundles", secret_key=b"mysecret")
server.auth.add_token("admin-token", "admin", ["upload", "download", "admin"])
```

## Client Example

```python
from kerbiancore.livepush.client import LivePushClient
client = LivePushClient(server, "client_bundles", pubkey=b"mysecret")
client.add_hook("post_update", lambda v: print("Updated to", v))
client.update("admin-token")
```

---

## CLI Usage

```
python -m kerbiancore.livepush.cli upload --token TOKEN --bundle path.tar.gz --version v1
python -m kerbiancore.livepush.cli inspect --token TOKEN
python -m kerbiancore.livepush.cli rollback --token TOKEN --target v0
```

---

## Security Model

- **Authentication:** All actions require a token with proper scope.
- **Signing:** All patches are signed (HMAC; use asymmetric for prod).
- **Verification:** Client verifies signature before applying update.
- **Atomicity:** Bundles are replaced atomically to avoid corruption.

---

## Integration Guide

- The bundle can be any tar.gz or zip; structure is up to you.
- Use hooks to run migrations, clear cache, etc before/after update.
- Implement staged rollout by customizing the server API or using A/B logic in client.
- Use monitor.py to track update events and failures for visibility.

---

## Best Practices

- Use strong, unique keys for signing.
- Rotate tokens periodically.
- Monitor update and error events.
- Test rollback and recovery flows before production rollout.

---