import threading

class AnalyticsTracker:
    def __init__(self):
        self.providers = []

    def register_provider(self, provider):
        self.providers.append(provider)

    def track_event(self, event_name, properties=None):
        for provider in self.providers:
            threading.Thread(target=provider.track_event, args=(event_name, properties or {})).start()

    def set_user(self, user_id, traits=None):
        for provider in self.providers:
            threading.Thread(target=provider.set_user, args=(user_id, traits or {})).start()


class ConsoleAnalyticsProvider:
    def track_event(self, event_name, properties):
        print(f"[Analytics] {event_name}: {properties}")

    def set_user(self, user_id, traits):
        print(f"[Analytics] Set user {user_id}: {traits}")

# Example: FirebaseAnalyticsProvider, MixpanelAnalyticsProvider can be created similarly