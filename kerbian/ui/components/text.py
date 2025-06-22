from kerbian.core.component import Component

class Text(Component):
    def render(self):
        return {
            "type": "text",
            "props": {
                "value": self.props.get("value") or (self.props.get("children", [""])[0] if self.props.get("children") else ""),
                "style": self.props.get("style", {}),
            },
            "children": [],
        }