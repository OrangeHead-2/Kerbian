import inspect

class Component:
    def __init__(self, **props):
        self.props = props
        self.state = {}
        self.children = props.get("children", [])
        self._update_callback = None
        self._hook_states = []
        self._hook_index = 0

    def set_state(self, new_state: dict):
        self.state.update(new_state)
        if self._update_callback:
            self._update_callback()

    def render(self):
        raise NotImplementedError

    def _start_render(self):
        self._hook_index = 0
        return self.render()

def is_component(obj):
    return isinstance(obj, Component) or callable(obj)

def render_component(obj, props=None):
    if isinstance(obj, Component):
        return obj._start_render()
    elif callable(obj):
        return obj(**(props or {}))
    else:
        raise TypeError(f"Cannot render object of type {type(obj)}")