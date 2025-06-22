class AndroidBridge:
    def initialize_app(self):
        raise NotImplementedError("AndroidBridge.initialize_app must be implemented")

    def create_native_tree(self, vdom):
        raise NotImplementedError("AndroidBridge.create_native_tree must be implemented")

    def mount_tree(self, tree):
        raise NotImplementedError("AndroidBridge.mount_tree must be implemented")

    def start_main_loop(self, update_callback):
        raise NotImplementedError("AndroidBridge.start_main_loop must be implemented")

    def update_tree(self, tree):
        raise NotImplementedError("AndroidBridge.update_tree must be implemented")