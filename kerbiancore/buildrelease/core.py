import os
import shutil
import zipfile
import time

class BuildConfig:
    def __init__(self, app_name, version, src_dir, build_dir, output_dir, platform, signing_info=None):
        self.app_name = app_name
        self.version = version
        self.src_dir = src_dir
        self.build_dir = build_dir
        self.output_dir = output_dir
        self.platform = platform
        self.signing_info = signing_info or {}

class BuildReleaseManager:
    def __init__(self):
        self.hooks = {"pre_build": [], "post_build": [], "pre_release": [], "post_release": []}

    def register_hook(self, stage, fn):
        if stage in self.hooks:
            self.hooks[stage].append(fn)

    def _run_hooks(self, stage, config):
        for fn in self.hooks.get(stage, []):
            try:
                fn(config)
            except Exception as e:
                print(f"[BuildRelease] Hook {stage} failed: {e}")

    def clean_build(self, config):
        if os.path.exists(config.build_dir):
            shutil.rmtree(config.build_dir)
        os.makedirs(config.build_dir, exist_ok=True)

    def copy_sources(self, config):
        if not os.path.isdir(config.src_dir):
            raise RuntimeError(f"Source dir {config.src_dir} not found")
        for root, dirs, files in os.walk(config.src_dir):
            rel = os.path.relpath(root, config.src_dir)
            dest_root = os.path.join(config.build_dir, rel)
            os.makedirs(dest_root, exist_ok=True)
            for f in files:
                shutil.copy2(os.path.join(root, f), os.path.join(dest_root, f))

    def package_app(self, config):
        timestamp = int(time.time())
        package_name = f"{config.app_name}-{config.version}-{config.platform}-{timestamp}.zip"
        package_path = os.path.join(config.output_dir, package_name)
        os.makedirs(config.output_dir, exist_ok=True)
        with zipfile.ZipFile(package_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(config.build_dir):
                for f in files:
                    full_path = os.path.join(root, f)
                    arcname = os.path.relpath(full_path, config.build_dir)
                    z.write(full_path, arcname)
        return package_path

    def sign_package(self, config, package_path):
        sign_info = config.signing_info
        # Dummy: add a .signed file as a marker.
        if sign_info:
            with open(package_path + ".signed", "w") as f:
                f.write(f"signed_by={sign_info.get('signer','unknown')}\n")
        return package_path + ".signed" if sign_info else package_path

    def build(self, config: BuildConfig):
        self._run_hooks("pre_build", config)
        self.clean_build(config)
        self.copy_sources(config)
        self._run_hooks("post_build", config)

        self._run_hooks("pre_release", config)
        package_path = self.package_app(config)
        signed_path = self.sign_package(config, package_path)
        self._run_hooks("post_release", config)
        return signed_path

    def upload_to_store(self, config, signed_package_path, store_credentials):
        # Dummy: write a file to simulate upload
        upload_id = int(time.time())
        upload_log = os.path.join(config.output_dir, f"upload-{upload_id}.log")
        with open(upload_log, "w") as f:
            f.write(f"Uploaded {signed_package_path} to {config.platform} store as {config.app_name} (credentials: {store_credentials})\n")
        print(f"[BuildRelease] Uploaded {signed_package_path} (simulated)")
        return upload_log