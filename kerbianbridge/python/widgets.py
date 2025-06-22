class Widget:
    def __init__(self, bridge, type_, props):
        self.bridge = bridge
        self.type = type_
        self.props = dict(props) if props else {}
        self.view_id = self.bridge.call("UIManager", "create_view", {"type": self.type, "props": self.props})

    def update(self, new_props):
        self.props.update(new_props)
        self.bridge.call("UIManager", "update_view", {"view_id": self.view_id, "props": self.props})

    def remove(self):
        self.bridge.call("UIManager", "remove_view", {"view_id": self.view_id})

class Button(Widget):
    def __init__(self, bridge, text, **kwargs):
        props = {"text": text}
        props.update(kwargs)
        super().__init__(bridge, "Button", props)

class Text(Widget):
    def __init__(self, bridge, value, **kwargs):
        props = {"value": value}
        props.update(kwargs)
        super().__init__(bridge, "Text", props)

class Image(Widget):
    def __init__(self, bridge, src, **kwargs):
        props = {"src": src}
        props.update(kwargs)
        super().__init__(bridge, "Image", props)

class List(Widget):
    def __init__(self, bridge, items, **kwargs):
        props = {"items": items}
        props.update(kwargs)
        super().__init__(bridge, "List", props)

class Modal(Widget):
    def __init__(self, bridge, message, **kwargs):
        props = {"message": message}
        props.update(kwargs)
        super().__init__(bridge, "Modal", props)