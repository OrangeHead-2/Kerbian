"""
KerbianCore Device: Push Notifications

- Push registration, token management, custom protocol/server
- Notification display, background handling, user actions
- Abstract interfaces for integration with native notification services
"""

import threading
from typing import Callable, Dict, Any, Optional, List

class PushTokenManager:
    def __init__(self):
        self.tokens = {}  # device_id -> token
        self.lock = threading.Lock()

    def register(self, device_id: str, token: str):
        with self.lock:
            self.tokens[device_id] = token

    def unregister(self, device_id: str):
        with self.lock:
            self.tokens.pop(device_id, None)

    def get_token(self, device_id: str) -> Optional[str]:
        with self.lock:
            return self.tokens.get(device_id)

    def all_tokens(self) -> List[str]:
        with self.lock:
            return list(self.tokens.values())

class PushServer:
    """
    Abstract push server - integrate with your push service provider.
    The send_fn must perform actual network delivery.
    """
    def __init__(self, send_fn: Callable[[str, Dict[str, Any]], bool]):
        self.send_fn = send_fn

    def send(self, token: str, message: Dict[str, Any]) -> bool:
        return self.send_fn(token, message)

    def broadcast(self, tokens: List[str], message: Dict[str, Any]) -> Dict[str, bool]:
        return {token: self.send(token, message) for token in tokens}

class NotificationManager:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def display(self, title: str, body: str, actions: Optional[List[Dict[str, Any]]] = None):
        """
        Display a notification to the user.
        Must be implemented using the native notification service for the platform.
        """
        raise NotImplementedError("Implement display() with native notification APIs for your platform.")

    def on_action(self, action: str, callback: Callable):
        self.handlers[action] = callback

    def handle_action(self, action: str, data: Any = None):
        cb = self.handlers.get(action)
        if cb:
            cb(data)

    def receive_push(self, message: Dict[str, Any]):
        """
        Process a push message. Calls display() and invokes actions if any.
        """
        self.display(
            message.get("title", ""),
            message.get("body", ""),
            message.get("actions")
        )
        if "action" in message:
            self.handle_action(message["action"], message.get("data"))