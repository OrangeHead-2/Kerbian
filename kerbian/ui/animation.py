class Animation:
    def __init__(self, properties, duration=300, curve="ease"):
        self.properties = properties
        self.duration = duration
        self.curve = curve
        self.on_complete = None

    def start(self, on_complete=None):
        self.on_complete = on_complete
        # Bridge to native async animation