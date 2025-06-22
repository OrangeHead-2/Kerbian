from typing import Callable, Any

class Store:
    def __init__(self, reducer: Callable, initial_state: Any):
        self.reducer = reducer
        self.state = initial_state
        self.subscribers = []

    def dispatch(self, action: Any):
        self.state = self.reducer(self.state, action)
        for sub in self.subscribers:
            sub(self.state)

    def subscribe(self, callback: Callable):
        self.subscribers.append(callback)
        return lambda: self.subscribers.remove(callback)

    def get_state(self):
        return self.state