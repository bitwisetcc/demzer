from django import template

register = template.Library()

@register.filter
def isint(value):
    return value % 1 == 0

@register.filter
def castint(value):
    return int(value)
