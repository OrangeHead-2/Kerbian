# Kerbian

Kerbian is a robust, secure, and scalable Python toolkit for mobile app development automation, profiling, testing, CI/CD, plugin management, and more.

## Features

- **Testing:** Unit testing, assertions, and reporting utilities.
- **Build/Release Automation:** Build, package, and deploy for Android/iOS.
- **Profiling:** Performance profiling for code sections and functions.
- **Security:** Secure storage, code audits, and secret management.
- **Plugins Ecosystem:** Registry, hub, and manager for plugins (local and remote).
- **CI/CD Templates:** Ready-to-use templates for popular mobile CI/CD platforms.
- **Community/Ecosystem:** Registry and hub for open/community plugins.

## Documentation

- [Docs Index](kerbiancore/docs/index.md)
- [Testing Module](kerbiancore/testing/README.md)
- [Build/Release Module](kerbiancore/buildrelease/README.md)
- [Profiling Module](kerbiancore/profiling/README.md)
- [Security Module](kerbiancore/security/README.md)
- [Plugins Module](kerbiancore/plugins/README.md)
- [CI/CD Module](kerbiancore/cicd/README.md)
- [Ecosystem](kerbiancore/ecosystem/README.md)

## Getting Started

```bash
pip install kerbiancore
```

Or clone and install locally:

```bash
git clone https://github.com/kerbiancore/kerbiancore.git
cd kerbiancore
pip install -e .
```

## Usage Example

```python
from kerbiancore.testing.core import test

@test
def my_test():
    assert 1 + 1 == 2
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

See [LICENSE](LICENSE)

---
