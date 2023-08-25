from django import template

register = template.Library()

@register.filter
def isint(value):
    return value % 1 == 0
