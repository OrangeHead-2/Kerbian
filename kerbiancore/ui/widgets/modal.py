"""
KerbianCore UI: Modal & Overlay Widgets

- Modal, BottomSheet, Popover, AlertDialog
- Custom overlays
- Animations, transitions, backdrop filters
"""

from kerbiancore.ui.core import Widget

class Modal(Widget):
    def __init__(self, content, on_close=None, **kwargs):
        super().__init__(props=kwargs)
        self.content = content
        self.on_close = on_close

    def close(self):
        if self.on_close:
            self.on_close()
        self.unmount()

    def render(self):
        # Render the modal content and backdrop
        self.children = [self.content]
        return self

class BottomSheet(Modal):
    pass  # Uses Modal, with special animation/position

class Popover(Modal):
    pass  # Uses Modal, positioned relative to anchor widget

class AlertDialog(Modal):
    def __init__(self, title, message, buttons, **kwargs):
        content = AlertDialogContent(title, message, buttons)
        super().__init__(content, **kwargs)

class AlertDialogContent(Widget):
    def __init__(self, title, message, buttons):
        super().__init__()
        self.title = title
        self.message = message
        self.buttons = buttons  # List of (label, callback)

    def render(self):
        # Pseudo-UI: title, message, buttons
        return self

class Overlay(Widget):
    def __init__(self, content, **kwargs):
        super().__init__(props=kwargs)
        self.content = content

    def render(self):
        self.children = [self.content]
        return self

# Animations, transitions, and backdrop filters are handled via the animation and theme modules.