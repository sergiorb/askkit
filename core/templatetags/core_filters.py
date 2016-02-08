from django import template
from users.models import STYLE_CHOICES
register = template.Library()

@register.filter
def to_class_name(value):
	return value.__class__.__name__.lower()


register = template.Library()

@register.filter
def style(q):
    for style in STYLE_CHOICES:
        if style[0] == q:
            return style[1]
    return ''