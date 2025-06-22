from kerbiancore.ui.core import UIWidget, UIEvent

class UITextInput(UIWidget):
    def __init__(self, value="", on_change=None, **props):
        super().__init__(**props)
        self.props['value'] = value
        self.on_change = on_change

    def render(self):
        return {"type": "TextInput", "id": self.id, "props": dict(self.props)}

    def change(self, new_value):
        self.props['value'] = new_value
        if self.on_change:
            evt = UIEvent("change", self.id, {"value": new_value})
            self.on_change(evt)

class UICheckbox(UIWidget):
    def __init__(self, checked=False, on_toggle=None, **props):
        super().__init__(**props)
        self.props['checked'] = checked
        self.on_toggle = on_toggle

    def render(self):
        return {"type": "Checkbox", "id": self.id, "props": dict(self.props)}

    def toggle(self):
        self.props['checked'] = not self.props['checked']
        if self.on_toggle:
            evt = UIEvent("toggle", self.id, {"checked": self.props['checked']})
            self.on_toggle(evt)