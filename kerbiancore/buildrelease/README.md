# KerbianCore Build/Release Module

Automate building, packaging, and releasing mobile apps for Android and iOS.

## Features

- `BuildConfig` for managing build parameters
- `BuildReleaseManager` for orchestrating builds and uploads
- Templates for Android/iOS and integration with app stores

## Example

```python
from kerbiancore.buildrelease.core import BuildConfig, BuildReleaseManager

cfg = BuildConfig(app_name="MyApp", version="1.0.0", ...)
mgr = BuildReleaseManager()
artifact = mgr.build(cfg)
mgr.upload_to_store(cfg, artifact)
```

- [Templates](./template_android.py), [./template_ios.py]
- [Tests](./tests.py)

---