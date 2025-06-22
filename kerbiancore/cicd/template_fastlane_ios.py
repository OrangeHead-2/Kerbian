FASTLANE_IOS = """
# Fastlane iOS Configuration (KerbianCore)
# Place this as fastlane/Fastfile in your iOS project

default_platform(:ios)

platform :ios do
  desc "Build and Release iOS IPA"
  lane :build_release do
    # Replace scheme and workspace with your own
    gym(
      scheme: "YourApp",
      workspace: "YourApp.xcworkspace"
    )
  end

  desc "Upload IPA to App Store (Replace with fastlane deliver config)"
  lane :deploy do
    build_release
    # deliver(
    #   submit_for_review: true,
    #   automatic_release: true
    # )
    puts "Simulate: Uploading IPA to App Store (replace with real upload)"
  end
end
"""