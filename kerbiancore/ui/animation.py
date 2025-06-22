"""
KerbianCore UI: Animation Engine

- Keyframe animations
- Transitions
- Gestures (swipe, tap, pinch)
"""

from typing import Callable, Dict, Any, Optional

class Animation:
    def __init__(self, keyframes: Dict[float, Dict[str, Any]], duration: float, on_update: Optional[Callable] = None, on_complete: Optional[Callable] = None):
        """
        keyframes: {progress (0.0-1.0): {prop: value}}
        duration: seconds
        """
        self.keyframes = keyframes
        self.duration = duration
        self.on_update = on_update
        self.on_complete = on_complete
        self.running = False

    def start(self):
        self.running = True
        # Pseudo-animation loop (real impl would use platform timer)
        import time
        start_time = time.time()
        while self.running:
            elapsed = time.time() - start_time
            progress = min(elapsed / self.duration, 1.0)
            frame = self.interpolate(progress)
            if self.on_update:
                self.on_update(frame)
            if progress >= 1.0:
                self.running = False
                if self.on_complete:
                    self.on_complete()
            time.sleep(0.016)  # ~60 FPS

    def stop(self):
        self.running = False

    def interpolate(self, progress):
        # Simple linear interpolation between defined keyframes
        keys = sorted(self.keyframes.keys())
        for i in range(1, len(keys)):
            if progress <= keys[i]:
                k0, k1 = keys[i-1], keys[i]
                f0, f1 = self.keyframes[k0], self.keyframes[k1]
                t = (progress - k0) / (k1 - k0) if k1 != k0 else 0
                return {prop: f0[prop] + t * (f1[prop] - f0[prop]) for prop in f0}
        return self.keyframes[keys[-1]]

class Gesture:
    def __init__(self, gesture_type: str, callback: Callable):
        self.gesture_type = gesture_type
        self.callback = callback

    def handle(self, event):
        if event.type == self.gesture_type:
            self.callback(event)

# Usage: attach Animation/Gesture to widget or UI controller as needed.