import sys
import threading
from kerbian.core.renderer import Renderer
from kerbian.core.component import Component
from kerbian.platform.common import get_platform_backend

class Application:
    def __init__(self, root_component: type):
        if not issubclass(root_component, Component):
            raise TypeError("Root component must be a subclass of Component")
        self.root_component_cls = root_component
        self.platform_backend = get_platform_backend()
        self.renderer = Renderer(self.platform_backend)
        self.running = False

    def run(self):
        self.running = True
        self.platform_backend.initialize_app()
        root_instance = self.root_component_cls()
        self.renderer.render(root_instance)
        self.platform_backend.start_main_loop(self._handle_update)

    def _handle_update(self):
        self.renderer.update()

def App(root_component):
    return Application(root_component)