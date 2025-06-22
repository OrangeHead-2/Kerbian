IOS_BUILD_TEMPLATE = """
# iOS Build/Release Script (KerbianCore)
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

echo "Building IPA (dummy, replace with Xcode build command)..."
cd "$BUILD_DIR"
zip -r "$OUTPUT_DIR/$APP_NAME-$VERSION-ios.zip" *

echo "Signing IPA (dummy, replace with codesign)..."
echo "signed" > "$OUTPUT_DIR/$APP_NAME-$VERSION-ios.zip.signed"
"""