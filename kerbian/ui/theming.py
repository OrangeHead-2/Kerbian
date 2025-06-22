class ThemeProvider:
    _current_theme = None
    _listeners = set()

    @classmethod
    def set_theme(cls, theme_name, palette):
        cls._current_theme = (theme_name, palette)
        for cb in cls._listeners:
            cb(theme_name, palette)

    @classmethod
    def get_theme(cls):
        return cls._current_theme

    @classmethod
    def subscribe(cls, callback):
        cls._listeners.add(callback)
        return lambda: cls._listeners.remove(callback)