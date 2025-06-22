class Route:
    def __init__(self, path, component, params=None):
        self.path = path
        self.component = component
        self.params = params or {}

class Router:
    def __init__(self):
        self.routes = {}
        self.stack = []

    def register(self, path, component):
        self.routes[path] = component

    def navigate(self, path, params=None):
        component = self.routes.get(path)
        if not component:
            raise Exception(f"Route {path} not found")
        self.stack.append(Route(path, component, params))
        self.render_current()

    def go_back(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.render_current()

    def render_current(self):
        if self.stack:
            current = self.stack[-1]
            # Dispatch render to current.component