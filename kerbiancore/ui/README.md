# KerbianCore UI — Production-quality Mobile Widgets

A cross-platform, pure-Python widget library for mobile UI.

---

## Features

- **Widget System:** Base class, lifecycle, event model, composition
- **Virtual DOM:** Efficient redraws via diffing engine
- **Lists & Grids:** ListView, GridView, infinite scroll, drag & drop, swipe actions, headers/footers
- **Modals & Overlays:** Modal, BottomSheet, Popover, AlertDialog, animated overlays
- **Forms:** Form builder, validation/input masks, dynamic and multi-step forms
- **Navigation:** NavigationBar, Tabs, Drawer, Stack navigation, deep linking
- **Media:** Image, Video, Audio, Camera preview, lazy loading
- **Theming:** Dynamic themes, runtime changes, dark/light mode, typography, spacing, accessibility
- **Animations:** Keyframe/transition animation, gestures (tap, swipe, pinch)
- **Extensible:** Compose and extend widgets; style and theme at runtime

---

## Usage

### Basic Widget

```python
from kerbiancore.ui.core import Widget

class MyLabel(Widget):
    def render(self):
        return self  # Custom render logic

label = MyLabel(props={"text": "Hello World"})
label.mount()
```

### ListView

```python
from kerbiancore.ui.widgets.list import ListView

def build_item(idx, item):
    return MyLabel(props={"text": str(item)})

listw = ListView(items=[1,2,3], item_builder=build_item)
listw.mount()
```

### Modal

```python
from kerbiancore.ui.widgets.modal import Modal

modal = Modal(content=MyLabel(props={"text": "This is a modal!"}))
modal.mount()
```

### Theming

```python
from kerbiancore.ui.theme import Theme
theme = Theme(mode="dark")
theme.apply(widget)
```

---

## Extending

- Subclass `Widget` for your own UI elements
- Use `add_event_listener` for custom events
- Implement custom themes, animations, gestures

---

## Catalog

- **Lists:** ListView, GridView, InfiniteScrollList, SectionedListView, DraggableListView, SwipeActionListView
- **Modals:** Modal, BottomSheet, Popover, AlertDialog, Overlay
- **Forms:** Form, DynamicForm, MultiStepForm, FormField
- **Navigation:** NavigationBar, Tabs, Drawer, StackNavigator, DeepLink
- **Media:** Image, Video, Audio, CameraPreview
- **Theme:** Theme engine, dynamic palette/typography/spacing
- **Animation:** Animation, Gesture

---

## Styling

- Use `Theme` to configure colors, typography, spacing
- Widgets receive theme via `props["theme"]`
- Override `render()` for custom drawing/styling

---

## Platform Support

- Designed to be platform-agnostic (backends: Kivy, PyQt, native mobile, or custom renderer)
- Widget tree and event model are pure Python

---

## Contributing

See main project CONTRIBUTING.md

---