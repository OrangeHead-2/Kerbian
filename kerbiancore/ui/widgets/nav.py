"""
KerbianCore UI: Navigation Widgets

- NavigationBar, Tabs, Drawer, Stack navigation, Deep linking
"""

from kerbiancore.ui.core import Widget

class NavigationBar(Widget):
    def __init__(self, items, on_select, selected=None, **kwargs):
        super().__init__(props=kwargs)
        self.items = items  # List of (icon, label)
        self.on_select = on_select
        self.selected = selected

    def select(self, idx):
        self.selected = idx
        self.on_select(idx)

    def render(self):
        # Render nav items
        return self

class Tabs(Widget):
    def __init__(self, tabs, on_tab_change, selected=0, **kwargs):
        super().__init__(props=kwargs)
        self.tabs = tabs  # List of (title, content)
        self.selected = selected
        self.on_tab_change = on_tab_change

    def change_tab(self, idx):
        self.selected = idx
        self.on_tab_change(idx)

    def render(self):
        # Render selected tab content
        return self

class Drawer(Widget):
    def __init__(self, content, open=False, on_toggle=None, **kwargs):
        super().__init__(props=kwargs)
        self.content = content
        self.open = open
        self.on_toggle = on_toggle

    def toggle(self):
        self.open = not self.open
        if self.on_toggle:
            self.on_toggle(self.open)

    def render(self):
        if self.open:
            self.children = [self.content]
        else:
            self.children = []
        return self

class StackNavigator(Widget):
    def __init__(self, screens, initial=0, **kwargs):
        super().__init__(props=kwargs)
        self.screens = screens  # List of Widget
        self.stack = [initial]

    def push(self, idx):
        self.stack.append(idx)
        self.update()

    def pop(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.update()

    def render(self):
        if self.stack:
            self.children = [self.screens[self.stack[-1]]]
        else:
            self.children = []
        return self

class DeepLink:
    # Utility for deep linking navigation state
    @staticmethod
    def parse(url: str):
        # Parse url to navigation state
        return url.split("/")