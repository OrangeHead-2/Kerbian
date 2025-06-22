import platform
from kerbian.platform.android.bridge import AndroidBridge
from kerbian.platform.ios.bridge import IOSBridge

def get_platform_backend():
    system = platform.system()
    if system == "Darwin":
        return IOSBridge()
    elif system == "Linux" or system == "Android":
        return AndroidBridge()
    else:
        raise NotImplementedError(f"Platform {system} not supported")