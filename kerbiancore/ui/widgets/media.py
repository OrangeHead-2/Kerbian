"""
KerbianCore UI: Media Widgets

- Image, Video, Audio, Camera preview
- Lazy loading
- Platform-agnostic interfaces for real media integration
"""

from kerbiancore.ui.core import Widget

class Image(Widget):
    def __init__(self, src, alt="", lazy=False, **kwargs):
        super().__init__(props=kwargs)
        self.src = src
        self.alt = alt
        self.lazy = lazy

    def render(self):
        """
        Render the image using the underlying platform's image view.
        Must be implemented by the platform-specific backend.
        """
        raise NotImplementedError("Image.render must be implemented for the target platform.")

class Video(Widget):
    def __init__(self, src, controls=True, autoplay=False, **kwargs):
        super().__init__(props=kwargs)
        self.src = src
        self.controls = controls
        self.autoplay = autoplay

    def render(self):
        """
        Render the video using the underlying platform's video view.
        Must be implemented by the platform-specific backend.
        """
        raise NotImplementedError("Video.render must be implemented for the target platform.")

class Audio(Widget):
    def __init__(self, src, controls=True, autoplay=False, **kwargs):
        super().__init__(props=kwargs)
        self.src = src
        self.controls = controls
        self.autoplay = autoplay

    def render(self):
        """
        Render the audio using the underlying platform's audio view.
        Must be implemented by the platform-specific backend.
        """
        raise NotImplementedError("Audio.render must be implemented for the target platform.")

class CameraPreview(Widget):
    def __init__(self, on_frame=None, **kwargs):
        super().__init__(props=kwargs)
        self.on_frame = on_frame

    def start(self):
        """
        Start the camera preview using the platform's camera API.
        Must be implemented by the platform-specific backend.
        """
        raise NotImplementedError("CameraPreview.start must be implemented for the target platform.")

    def stop(self):
        """
        Stop the camera preview.
        Must be implemented by the platform-specific backend.
        """
        raise NotImplementedError("CameraPreview.stop must be implemented for the target platform.")

    def render(self):
        """
        Render the camera preview widget.
        Must be implemented by the platform-specific backend.
        """
        raise NotImplementedError("CameraPreview.render must be implemented for the target platform.")