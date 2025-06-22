ANDROID_BUILD_TEMPLATE = """
# Android Build/Release Script (KerbianCore)
export APP_NAME="{app_name}"
export VERSION="{version}"
export SRC_DIR="{src_dir}"
export BUILD_DIR="{build_dir}"
export OUTPUT_DIR="{output_dir}"

echo "Cleaning build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "Copying sources..."
cp -r "$SRC_DIR/"* "$BUILD_DIR/"

echo "Building APK (dummy, replace with actual build step)..."
cd "$BUILD_DIR"
zip -r "$OUTPUT_DIR/$APP_NAME-$VERSION-android.zip" *

echo "Signing APK (dummy, replace with jarsigner or apksigner)..."
echo "signed" > "$OUTPUT_DIR/$APP_NAME-$VERSION-android.zip.signed"
"""