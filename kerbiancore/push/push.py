import threading
import uuid
import time

class PushNotification:
    def __init__(self, title, body, data=None, to=None, priority="normal", sound=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.body = body
        self.data = data or {}
        self.timestamp = time.time()
        self.to = to  # None means broadcast, else user_id
        self.priority = priority
        self.sound = sound

class PushServer:
    def __init__(self):
        self.subscribers = {}
        self.lock = threading.Lock()
        self.history = []

    def subscribe(self, user_id, callback):
        with self.lock:
            if user_id not in self.subscribers:
                self.subscribers[user_id] = []
            self.subscribers[user_id].append(callback)

    def unsubscribe(self, user_id, callback):
        with self.lock:
            if user_id in self.subscribers:
                if callback in self.subscribers[user_id]:
                    self.subscribers[user_id].remove(callback)
                if not self.subscribers[user_id]:
                    del self.subscribers[user_id]

    def send(self, notification):
        with self.lock:
            self.history.append(notification)
            targets = [notification.to] if notification.to else list(self.subscribers.keys())
            for user_id in targets:
                for cb in self.subscribers.get(user_id, []):
                    try:
                        cb(notification)
                    except Exception as e:
                        print(f"[Push] Exception in subscriber for {user_id}: {e}")

    def get_history(self, limit=50):
        with self.lock:
            return list(self.history)[-limit:]