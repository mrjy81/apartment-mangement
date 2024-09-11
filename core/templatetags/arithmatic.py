# my_app/templatetags/my_custom_filters.py
from django import template
from core.helper import format_float

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter
def mult(value, arg):
    return float(value) * float(arg)


@register.filter
def add(value, arg):
    return float(value) + float(arg)


@register.filter
def subtract(value, arg):
    return float(value) - float(arg)


@register.filter
def formating_float(value):
    return format_float(value)
