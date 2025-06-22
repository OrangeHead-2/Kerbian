class IOSBridge:
    def initialize_app(self):
        raise NotImplementedError("IOSBridge.initialize_app must be implemented")

    def create_native_tree(self, vdom):
        raise NotImplementedError("IOSBridge.create_native_tree must be implemented")

    def mount_tree(self, tree):
        raise NotImplementedError("IOSBridge.mount_tree must be implemented")

    def start_main_loop(self, update_callback):
        raise NotImplementedError("IOSBridge.start_main_loop must be implemented")

    def update_tree(self, tree):
        raise NotImplementedError("IOSBridge.update_tree must be implemented")