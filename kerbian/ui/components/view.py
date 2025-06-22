from kerbian.core.component import Component

class View(Component):
    def render(self):
        children = self.props.get("children", [])
        return {
            "type": "view",
            "props": {
                "style": self.props.get("style", {}),
            },
            "children": [
                child._start_render() if isinstance(child, Component) else child for child in children
            ],
        }