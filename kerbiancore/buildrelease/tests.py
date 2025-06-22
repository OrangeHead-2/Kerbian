"""
Unit tests for kerbiancore.buildrelease module.
"""

from kerbiancore.buildrelease.core import BuildConfig, BuildReleaseManager

def test_buildconfig_fields():
    cfg = BuildConfig(
        app_name="TestApp",
        version="0.1.2",
        src_dir="./src",
        build_dir="./build",
        output_dir="./dist",
        platform="android",
        signing_info={"signer": "test"}
    )
    assert cfg.app_name == "TestApp"
    assert cfg.platform == "android"
    assert isinstance(cfg.signing_info, dict)

def test_buildrelease_manager_sim():
    cfg = BuildConfig(
        app_name="TestApp",
        version="0.1.2",
        src_dir="./src",
        build_dir="./build",
        output_dir="./dist",
        platform="android",
        signing_info={"signer": "test"}
    )
    mgr = BuildReleaseManager()
    # Simulated build returns a file path or similar string
    artifact = mgr.build(cfg)
    assert artifact
    # Simulate upload (should not raise error)
    mgr.upload_to_store(cfg, artifact, store_credentials="dummy")

if __name__ == "__main__":
    test_buildconfig_fields()
    test_buildrelease_manager_sim()
    print("BuildRelease tests passed.")