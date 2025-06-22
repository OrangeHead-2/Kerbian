# KerbianCore Ecosystem Module

The Ecosystem module manages plugin discovery, registration, hub, and installation.

## Key Components

- **Registry**: Persistent record of plugins (local or remote)
- **Hub**: In-memory runtime registry for live plugin objects
- **Installer**: Loads plugins from file or URL
- **Manager**: High-level interface for all plugin operations

## Quickstart

```python
from kerbiancore.ecosystem.manager import EcosystemManager

eco = EcosystemManager()
eco.hub.add_plugin("my_plugin", lambda name: print(f"Hi, {name}"))
eco.run_plugin("my_plugin", "KerbianCore")
```

## Structure

- `registry.py` — JSON registry of plugins
- `hub.py` — In-memory hub for runtime plugins
- `installer.py` — Load plugins from local/remote files
- `manager.py` — Unified management interface

## Docs

- [COMMUNITY.md](./COMMUNITY.md)
- [HUB.md](./HUB.md)
- [MANAGER.md](./MANAGER.md)
- [EXAMPLES.md](./EXAMPLES.md)
- [TESTS.md](./TESTS.md)

---