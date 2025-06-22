# KerbianCore CI/CD Templates for Mobile

## GitHub Actions: Android

- See `kerbiancore/cicd/templates.py` for copy-paste YAML.

## GitHub Actions: iOS

- See `kerbiancore/cicd/templates.py` for copy-paste YAML.

## Fastlane

- See `kerbiancore/cicd/template_fastlane_android.py` and `template_fastlane_ios.py`.

## Cross-platform

- Use matrix builds for both Android and iOS.

---

1. Copy template YAML into `.github/workflows/android.yml` or `.github/workflows/ios.yml`.
2. Adapt the build/upload step for your environment.
3. Use your own secrets for signing and store upload.

---

- For full mobile DevOps, combine with KerbianCore build/release and testing modules.

---