"""
KerbianCore UI Core

- Widget base class
- Widget lifecycle (init, mount, update, unmount)
- Event model (event bubbling, listeners)
- Widget composition (children)
- Virtual DOM and diffing engine (efficient redraw)
"""

from typing import Any, Callable, Dict, List, Optional, Union

class Event:
    def __init__(self, type_: str, target, data=None):
        self.type = type_
        self.target = target
        self.data = data
        self.propagation_stopped = False

    def stop_propagation(self):
        self.propagation_stopped = True

class Widget:
    def __init__(self, props: Optional[Dict[str, Any]] = None, children: Optional[List['Widget']] = None):
        self.props = props or {}
        self.children = children or []
        self.parent = None
        self._mounted = False
        self._event_listeners: Dict[str, List[Callable]] = {}

    def mount(self, parent=None):
        self.parent = parent
        self._mounted = True
        for child in self.children:
            child.mount(parent=self)
        self.on_mount()

    def update(self, new_props: Optional[Dict[str, Any]] = None):
        if new_props:
            self.props.update(new_props)
        self.on_update()

    def unmount(self):
        for child in self.children:
            child.unmount()
        self._mounted = False
        self.on_unmount()

    def add_event_listener(self, event_type: str, cb: Callable):
        if event_type not in self._event_listeners:
            self._event_listeners[event_type] = []
        self._event_listeners[event_type].append(cb)

    def remove_event_listener(self, event_type: str, cb: Callable):
        if event_type in self._event_listeners:
            self._event_listeners[event_type].remove(cb)

    def dispatch_event(self, event: Event):
        if event.type in self._event_listeners:
            for cb in self._event_listeners[event.type]:
                cb(event)
                if event.propagation_stopped:
                    break
        if not event.propagation_stopped and self.parent:
            self.parent.dispatch_event(event)

    # Virtual DOM: Widget tree diffing for efficient redraw
    def render(self):
        return self

    def diff(self, other: 'Widget') -> bool:
        # Returns True if self and other differ in type or props (not deep diff!)
        if type(self) != type(other):
            return True
        if self.props != other.props:
            return True
        if len(self.children) != len(other.children):
            return True
        for sc, oc in zip(self.children, other.children):
            if sc.diff(oc):
                return True
        return False

    # Lifecycle hooks
    def on_mount(self): pass
    def on_update(self): pass
    def on_unmount(self): pass

# Usage: subclass Widget for custom widgets and override render/lifecycle as needed.