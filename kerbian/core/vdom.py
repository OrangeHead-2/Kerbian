class VNode:
    def __init__(self, type_, props=None, children=None):
        self.type = type_
        self.props = props or {}
        self.children = []
        for child in (children or []):
            if isinstance(child, list):
                self.children.extend(child)
            elif child is not None:
                self.children.append(child)

def create_element(type_, props=None, *children):
    return VNode(type_, props, children)

class Fragment:
    pass