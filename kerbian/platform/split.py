import platform
import importlib

def current_platform():
    sys_platform = platform.system().lower()
    if "darwin" in sys_platform:
        return "ios"
    elif "linux" in sys_platform or "android" in sys_platform:
        return "android"
    elif "windows" in sys_platform:
        return "windows"
    return "unknown"

def import_platform_module(mod_basename):
    plat = current_platform()
    try:
        return importlib.import_module(f"{mod_basename}_{plat}")
    except ImportError:
        return importlib.import_module(mod_basename)

# Usage example:
# views = import_platform_module("kerbian.views.profile")
# This imports kerbian/views/profile_android.py or kerbian/views/profile_ios.py if present,
# falling back to kerbian/views/profile.py otherwise.