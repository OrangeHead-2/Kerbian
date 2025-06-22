from kerbian.core.component import Component, is_component, render_component
from kerbian.core.hooks import _set_current_component, _unset_current_component

class Renderer:
    def __init__(self, platform_backend):
        self.platform_backend = platform_backend
        self.tree = None

    def render(self, component):
        try:
            if isinstance(component, Component):
                _set_current_component(component)
                vdom = component._start_render()
                _unset_current_component()
                component._update_callback = lambda: self.update()
            elif callable(component):
                vdom = component()
            else:
                vdom = component
            self.tree = self.platform_backend.create_native_tree(vdom)
            self.platform_backend.mount_tree(self.tree)
        except Exception as e:
            # Error boundary: show a fallback UI or log
            print("Renderer error:", e)

    def update(self):
        if self.tree:
            self.platform_backend.update_tree(self.tree)