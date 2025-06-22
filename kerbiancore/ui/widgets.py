from kerbiancore.ui.core import UIWidget, UIEvent

class UILabel(UIWidget):
    def __init__(self, text, **props):
        super().__init__(**props)
        self.props['text'] = text

    def set_text(self, text):
        self.props['text'] = text

    def render(self):
        return {"type": "Label", "id": self.id, "props": dict(self.props)}

class UIButton(UIWidget):
    def __init__(self, text, on_press=None, **props):
        super().__init__(**props)
        self.props['text'] = text
        self.on_press = on_press

    def render(self):
        return {"type": "Button", "id": self.id, "props": dict(self.props)}

    def press(self):
        if self.on_press:
            evt = UIEvent("press", self.id)
            self.on_press(evt)

class UIImage(UIWidget):
    def __init__(self, path, **props):
        super().__init__(**props)
        self.props['path'] = path

    def render(self):
        return {"type": "Image", "id": self.id, "props": dict(self.props)}

class UIList(UIWidget):
    def __init__(self, items, on_select=None, **props):
        super().__init__(**props)
        self.items = list(items)
        self.on_select = on_select

    def set_items(self, items):
        self.items = list(items)

    def render(self):
        return {
            "type": "List",
            "id": self.id,
            "props": dict(self.props),
            "items": list(self.items),
        }

    def select(self, index):
        if self.on_select and 0 <= index < len(self.items):
            evt = UIEvent("select", self.id, {"index": index, "item": self.items[index]})
            self.on_select(evt)

class UIModal(UIWidget):
    def __init__(self, title, content, on_close=None, **props):
        super().__init__(**props)
        self.props['title'] = title
        self.props['content'] = content
        self.on_close = on_close

    def render(self):
        return {"type": "Modal", "id": self.id, "props": dict(self.props)}

    def close(self):
        if self.on_close:
            evt = UIEvent("close", self.id)
            self.on_close(evt)