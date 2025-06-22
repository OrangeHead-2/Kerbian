"""
KerbianCore UI: List & Grid Widgets

- ListView, GridView
- Infinite scroll
- Drag & drop, swipe actions
- Section headers, footers, sticky items
"""

from kerbiancore.ui.core import Widget, Event

class ListView(Widget):
    def __init__(self, items, item_builder, **kwargs):
        super().__init__(props=kwargs)
        self.items = items
        self.item_builder = item_builder  # function(index, item) -> Widget

    def render(self):
        self.children = [self.item_builder(i, item) for i, item in enumerate(self.items)]
        return self

class GridView(Widget):
    def __init__(self, items, item_builder, columns=2, **kwargs):
        super().__init__(props=kwargs)
        self.items = items
        self.item_builder = item_builder
        self.columns = columns

    def render(self):
        # Group items into rows
        self.children = []
        row = []
        for i, item in enumerate(self.items):
            row.append(self.item_builder(i, item))
            if (i+1) % self.columns == 0 or i == len(self.items)-1:
                self.children.append(RowWidget(row))
                row = []
        return self

class RowWidget(Widget):
    def __init__(self, children):
        super().__init__(children=children)

class InfiniteScrollList(ListView):
    def __init__(self, items, item_builder, load_more_cb, **kwargs):
        super().__init__(items, item_builder, **kwargs)
        self.load_more_cb = load_more_cb

    def on_scroll_to_bottom(self):
        # Call load_more_cb and update list
        more = self.load_more_cb()
        self.items.extend(more)
        self.update()  # Triggers re-render

class DraggableListView(ListView):
    def __init__(self, items, item_builder, on_reorder, **kwargs):
        super().__init__(items, item_builder, **kwargs)
        self.on_reorder = on_reorder

    def on_drag(self, from_idx, to_idx):
        item = self.items.pop(from_idx)
        self.items.insert(to_idx, item)
        self.on_reorder(self.items)
        self.update()

class SwipeActionListView(ListView):
    def __init__(self, items, item_builder, on_swipe, **kwargs):
        super().__init__(items, item_builder, **kwargs)
        self.on_swipe = on_swipe

    def on_swipe_item(self, idx, direction):
        self.on_swipe(idx, direction)

class SectionedListView(ListView):
    def __init__(self, sections, item_builder, header_builder=None, footer_builder=None, **kwargs):
        super().__init__([], item_builder, **kwargs)
        self.sections = sections  # [{header:..., items:[...], footer:...}]
        self.header_builder = header_builder
        self.footer_builder = footer_builder

    def render(self):
        self.children = []
        for section in self.sections:
            if self.header_builder and section.get("header"):
                self.children.append(self.header_builder(section["header"]))
            for i, item in enumerate(section.get("items", [])):
                self.children.append(self.item_builder(i, item))
            if self.footer_builder and section.get("footer"):
                self.children.append(self.footer_builder(section["footer"]))
        return self

# Sticky items could be handled in the rendering logic/UI layer.