````markdown
# Guide: Build/Release Automation for App Stores

## Android

1. **Set up `BuildConfig` and use `BuildReleaseManager` to package your APK**
2. **Sign APK manually or with Fastlane (see template)**
3. **Upload to Google Play (simulate or use Fastlane)**
4. **Automate with GitHub Actions or any CI using provided templates**

**Example:**

```python
from kerbiancore.buildrelease.core import BuildConfig, BuildReleaseManager

config = BuildConfig(
    app_name="MyApp",
    version="1.0.0",
    src_dir="./src",
    build_dir="./build",
    output_dir="./dist",
    platform="android",
    signing_info={"signer": "dev"}
)
mgr = BuildReleaseManager()
apk = mgr.build(config)
mgr.upload_to_store(config, apk, store_credentials="user:pass")