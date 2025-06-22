"""
KerbianCore UI: Form Widgets

- Form builder
- Validation rules, input masks
- Dynamic fields
- Multi-step forms, wizards
"""

from kerbiancore.ui.core import Widget

class Form(Widget):
    def __init__(self, fields, on_submit, validators=None, **kwargs):
        super().__init__(props=kwargs)
        self.fields = fields  # List of FormField
        self.on_submit = on_submit
        self.validators = validators or []

    def validate(self):
        errors = []
        for field in self.fields:
            err = field.validate()
            if err:
                errors.append((field.props.get("name"), err))
        for v in self.validators:
            err = v(self.fields)
            if err:
                errors.append(("form", err))
        return errors

    def submit(self):
        errors = self.validate()
        if errors:
            self.props["on_error"](errors) if "on_error" in self.props else None
        else:
            values = {f.props.get("name"): f.get_value() for f in self.fields}
            self.on_submit(values)

    def render(self):
        self.children = self.fields
        return self

class FormField(Widget):
    def __init__(self, name, input_type="text", label=None, value=None, validator=None, mask=None, **kwargs):
        super().__init__(props=kwargs)
        self.props["name"] = name
        self.props["input_type"] = input_type
        self.props["label"] = label or name
        self.value = value
        self.validator = validator
        self.mask = mask

    def validate(self):
        if self.validator:
            return self.validator(self.value)
        return None

    def get_value(self):
        return self.value

class DynamicForm(Form):
    def __init__(self, field_builder, schema, on_submit, **kwargs):
        # field_builder: function(schema) -> list of FormField
        fields = field_builder(schema)
        super().__init__(fields, on_submit, **kwargs)

class MultiStepForm(Widget):
    def __init__(self, steps, on_complete, **kwargs):
        super().__init__(props=kwargs)
        self.steps = steps  # List of Form
        self.current = 0
        self.on_complete = on_complete

    def next(self):
        if self.current < len(self.steps) - 1:
            self.current += 1
        else:
            values = {}
            for step in self.steps:
                values.update({f.props.get("name"): f.get_value() for f in step.fields})
            self.on_complete(values)

    def render(self):
        self.children = [self.steps[self.current]]
        return self

# Input masks and validation can be extended as needed.