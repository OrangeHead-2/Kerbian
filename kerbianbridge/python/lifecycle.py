class ViewLifecycleManager:
    def __init__(self):
        self._mounted = set()
        self._callbacks = {}

    def mount(self, view_id, callback=None):
        self._mounted.add(view_id)
        if callback:
            self._callbacks[view_id] = callback

    def unmount(self, view_id):
        self._mounted.discard(view_id)
        cb = self._callbacks.pop(view_id, None)
        if cb:
            try:
                cb()
            except Exception as e:
                print(f"Error in unmount callback for {view_id}: {e}")

    def is_mounted(self, view_id):
        return view_id in self._mounted