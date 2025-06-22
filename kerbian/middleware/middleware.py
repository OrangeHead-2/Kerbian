class MiddlewareManager:
    def __init__(self):
        self.middlewares = []

    def add(self, middleware):
        self.middlewares.append(middleware)

    def process(self, event, data):
        for mw in self.middlewares:
            data = mw(event, data)
        return data

middleware_manager = MiddlewareManager()