"""
KerbianCore Device: Sensors API

- Camera, GPS, accelerometer, gyroscope, microphone
- Permission abstraction, event listeners, calibration
- Platform-agnostic interfaces for real sensor integration
"""

from typing import Callable, Any, Dict, Optional

class PermissionError(Exception):
    pass

class PermissionManager:
    """
    Abstracts OS-level sensor permission requests.
    """
    def __init__(self):
        self.permissions = {}

    def request(self, sensor: str) -> bool:
        """
        Request permission for a specific sensor.
        Must be implemented using platform APIs.
        """
        raise NotImplementedError("Permission request must be implemented for each platform.")

    def check(self, sensor: str) -> bool:
        """
        Check if permission was granted for a specific sensor.
        Must be implemented using platform APIs.
        """
        raise NotImplementedError("Permission check must be implemented for each platform.")

class Sensor:
    """
    Platform-agnostic sensor base class.
    Override for platform-specific implementation.
    """
    def __init__(self, name: str, permission_manager: PermissionManager):
        self.name = name
        self.listeners = []
        self.permission_manager = permission_manager

    def add_listener(self, cb: Callable[[Any], None]):
        self.listeners.append(cb)

    def remove_listener(self, cb: Callable[[Any], None]):
        self.listeners.remove(cb)

    def emit(self, data):
        for cb in self.listeners:
            cb(data)

    def start(self):
        """
        Start the sensor.
        Must be implemented using platform APIs.
        """
        raise NotImplementedError("Sensor.start must be implemented for each platform.")

    def stop(self):
        """
        Stop the sensor.
        Must be implemented using platform APIs.
        """
        raise NotImplementedError("Sensor.stop must be implemented for each platform.")

class Camera(Sensor):
    def __init__(self, permission_manager: PermissionManager):
        super().__init__("camera", permission_manager)

    def capture(self):
        """
        Capture an image from the camera.
        Must be implemented using platform APIs.
        """
        raise NotImplementedError("Camera.capture must be implemented for each platform.")

class GPS(Sensor):
    def __init__(self, permission_manager: PermissionManager):
        super().__init__("gps", permission_manager)

    def update_position(self, lat, lon):
        """
        Update GPS position. Typically called by platform event hooks.
        """
        raise NotImplementedError("GPS.update_position must be implemented for each platform.")

class Accelerometer(Sensor):
    def __init__(self, permission_manager: PermissionManager):
        super().__init__("accelerometer", permission_manager)

    def update(self, x, y, z):
        """
        Update accelerometer reading.
        """
        raise NotImplementedError("Accelerometer.update must be implemented for each platform.")

class Gyroscope(Sensor):
    def __init__(self, permission_manager: PermissionManager):
        super().__init__("gyroscope", permission_manager)

    def update(self, x, y, z):
        """
        Update gyroscope reading.
        """
        raise NotImplementedError("Gyroscope.update must be implemented for each platform.")

class Microphone(Sensor):
    def __init__(self, permission_manager: PermissionManager):
        super().__init__("microphone", permission_manager)

    def record(self):
        """
        Start microphone recording.
        Must be implemented using platform APIs.
        """
        raise NotImplementedError("Microphone.record must be implemented for each platform.")