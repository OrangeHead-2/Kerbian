# Integrating KerbianBridge into Your Mobile App

## Android

1. Add `KerbianBridge.java`, `UIManager.java`, and all modules to your Android app in `app/src/main/java/kerbianbridge/android/`.
2. In your `MainActivity`, start the bridge server:
   ```java
   KerbianBridge bridge = new KerbianBridge(8123);
   bridge.start();
   ```
3. Ensure your app requests the necessary permissions for networking and file access.

## iOS

1. Add `KerbianBridge.{h,m}`, `UIManager.{h,m}`, all modules, and bridge router to your Xcode project.
2. In your app delegate, start the bridge server:
   ```objectivec
   KerbianBridge *bridge = [[KerbianBridge alloc] initWithPort:8123];
   [bridge start];
   ```
3. Add necessary Info.plist entries for networking.

## Python

1. Use `NativeBridgeClient` to connect and send/receive messages:
   ```python
   from kerbianbridge.python.bridge import NativeBridgeClient
   bridge = NativeBridgeClient(port=8123)
   # Create button:
   btn_id = bridge.call("UIManager", "create_view", {"type": "Button", "props": {"text": "Hi"}})
   # Handle events:
   bridge.on_event("onPress", lambda view_id, data: print("Button pressed!"))
   ```

## Event Routing

- UI events (e.g., button press) are sent from native to Python as event messages.
- Python can send commands to update or remove views at any time.
- Lifecycle:
  - Use `create_view`, `update_view`, `remove_view` for mount/update/unmount.
  - Error messages are sent as JSON lines with `"type": "error"`.

## Error Reporting

- Use `bridge.report_error("ViewError", "Failed to update view", {...})` in Python.
- Native code should send error JSON lines to the Python socket.

## Bidirectional Modules

- Register Python modules via `bridge.register_module("MyModule", mymodule)`.
- Native can call Python methods on registered modules by sending a `"type": "call"` message.
