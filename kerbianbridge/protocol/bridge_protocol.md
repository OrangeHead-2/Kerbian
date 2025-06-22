# KerbianBridge Protocol

All communication between Python and native occurs over a simple line-based message protocol (via sockets or pipes):

- Each message is a JSON object, one per line.
- Messages have `type` (e.g., "call", "event", "response"), `target` (module/class), `method`, and `args`
- The protocol is symmetrical: Python can call native, and vice versa.

**Example:**

```json
{
  "type": "call",
  "target": "UIManager",
  "method": "create_view",
  "args": {
    "type": "Button",
    "props": {
      "text": "Click me"
    }
  }
}
```

Native responds:

```json
{
  "type": "response",
  "id": 123,
  "result": {"view_id": 7}
}
```