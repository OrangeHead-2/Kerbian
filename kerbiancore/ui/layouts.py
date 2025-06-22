from kerbiancore.ui.core import UIWidget

class UIColumn(UIWidget):
    def __init__(self, *children, **props):
        super().__init__(**props)
        for child in children:
            self.add_child(child)

    def render(self):
        return {
            "type": "Column",
            "id": self.id,
            "props": dict(self.props),
            "children": [child.render() for child in self.children]
        }

class UIRow(UIWidget):
    def __init__(self, *children, **props):
        super().__init__(**props)
        for child in children:
            self.add_child(child)

    def render(self):
        return {
            "type": "Row",
            "id": self.id,
            "props": dict(self.props),
            "children": [child.render() for child in self.children]
        }

class UIStack(UIWidget):
    def __init__(self, *children, **props):
        super().__init__(**props)
        for child in children:
            self.add_child(child)

    def render(self):
        return {
            "type": "Stack",
            "id": self.id,
            "props": dict(self.props),
            "children": [child.render() for child in self.children]
        }