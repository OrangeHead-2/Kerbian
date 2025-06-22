FASTLANE_ANDROID = """
# Fastlane Android Configuration (KerbianCore)
# Place this as fastlane/Fastfile in your Android project

default_platform(:android)

platform :android do
  desc "Build and Release Android APK"
  lane :build_release do
    gradle(
      task: "assemble",
      build_type: "Release"
    )
    # Optionally sign your APK here
    # sh "apksigner sign --ks your.keystore app-release.apk"
  end

  desc "Upload APK to Google Play (Replace with fastlane supply config)"
  lane :deploy do
    build_release
    # supply(
    #   track: "production",
    #   apk: "app/build/outputs/apk/release/app-release.apk"
    # )
    puts "Simulate: Uploading APK to Play Store (replace with real upload)"
  end
end
"""