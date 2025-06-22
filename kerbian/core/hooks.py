from typing import Any, Callable, Tuple

__current_component = None

def useState(initial_value: Any) -> Tuple[Any, Callable[[Any], None]]:
    component = __current_component
    if component is None:
        raise RuntimeError("useState() called outside of component context")
    idx = component._hook_index
    if idx >= len(component._hook_states):
        component._hook_states.append(initial_value)
    value = component._hook_states[idx]
    def set_value(new_value):
        component._hook_states[idx] = new_value
        if component._update_callback:
            component._update_callback()
    component._hook_index += 1
    return (value, set_value)

def _set_current_component(component):
    global __current_component
    __current_component = component

def _unset_current_component():
    global __current_component
    __current_component = None