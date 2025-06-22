ANDROID_CI_YML = """
# Android CI Pipeline (KerbianCore)
name: Android Build & Release

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up JDK
      uses: actions/setup-java@v4
      with:
        distribution: 'temurin'
        java-version: '17'

    - name: Build with Gradle (replace with real build)
      run: ./gradlew assembleDebug

    - name: Archive APK
      uses: actions/upload-artifact@v4
      with:
        name: app-debug
        path: app/build/outputs/apk/debug/app-debug.apk
"""

IOS_CI_YML = """
# iOS CI Pipeline (KerbianCore)
name: iOS Build & Release

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: macos-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Xcode
      run: sudo xcode-select -s /Applications/Xcode_15.0.app

    - name: Build IPA (dummy, replace with xcodebuild)
      run: echo "xcodebuild -scheme YourApp -configuration Release"

    - name: Archive IPA
      uses: actions/upload-artifact@v4
      with:
        name: app-release
        path: path/to/app.ipa
"""

CROSSPLATFORM_CI_YML = """
# Cross-platform Mobile CI/CD (KerbianCore)
name: Mobile Build Matrix

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Set up Environment
      run: echo "Set up Android or iOS toolchain here."

    - name: Build
      run: echo "Insert build command for ${{ matrix.os }}"

    - name: Archive Build
      uses: actions/upload-artifact@v4
      with:
        name: app-build
        path: path/to/artifact
"""