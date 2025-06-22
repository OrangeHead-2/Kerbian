from kerbian.core.component import Component

class Button(Component):
    def render(self):
        return {
            "type": "button",
            "props": {
                "text": self.props.get("text", ""),
                "onPress": self.props.get("onPress"),
                "style": self.props.get("style", {}),
            },
            "children": [],
        }