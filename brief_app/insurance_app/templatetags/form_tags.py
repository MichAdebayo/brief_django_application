# from django import template
# from django.forms.boundfield import BoundField  # Import BoundField

# register = template.Library()

# @register.filter(name='add_class')
# def add_class(value: BoundField, arg: str) -> BoundField:
#     css_classes = value.field.widget.attrs.get('class', '')
#     css_classes = f"{css_classes} {arg}" if css_classes else arg
#     return value.as_widget(attrs={'class': css_classes})


from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """Adds a CSS class to a form field."""
    try:
        css_classes = value.field.widget.attrs.get('class', '')
        css_classes = f"{css_classes} {arg}" if css_classes else arg
        return value.as_widget(attrs={'class': css_classes})
    except AttributeError:
        # Handle cases where value is not a BoundField (e.g., during testing)
        return value