"""
KerbianCore UI: Theming Engine

- Dynamic runtime themes (dark/light, custom palettes)
- Typography, spacing, adaptive layouts
- Accessibility support
"""

class Theme:
    def __init__(self, palette=None, typography=None, spacing=None, mode="light"):
        self.palette = palette or Theme.default_palette(mode)
        self.typography = typography or Theme.default_typography()
        self.spacing = spacing or Theme.default_spacing()
        self.mode = mode

    @staticmethod
    def default_palette(mode):
        if mode == "dark":
            return {
                "background": "#222",
                "foreground": "#fff",
                "primary": "#1e90ff",
                "secondary": "#888",
            }
        return {
            "background": "#fff",
            "foreground": "#222",
            "primary": "#1e90ff",
            "secondary": "#888",
        }

    @staticmethod
    def default_typography():
        return {
            "fontFamily": "System",
            "fontSize": 16,
            "fontWeight": "normal",
        }

    @staticmethod
    def default_spacing():
        return {
            "padding": 8,
            "margin": 8,
        }

    def set_mode(self, mode):
        self.mode = mode
        self.palette = Theme.default_palette(mode)

    def update_palette(self, new_palette):
        self.palette.update(new_palette)

    def update_typography(self, new_typography):
        self.typography.update(new_typography)

    def update_spacing(self, new_spacing):
        self.spacing.update(new_spacing)

    def apply(self, widget):
        # Apply theme to widget and children recursively
        if hasattr(widget, "props"):
            widget.props["theme"] = self
        for child in getattr(widget, "children", []):
            self.apply(child)

# Accessibility helpers could be added as needed.