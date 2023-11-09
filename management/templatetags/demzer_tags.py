from django import template

register = template.Library()

@register.filter
def isint(value):
    return value % 1 == 0

@register.filter
def castint(value):
    return int(value) if value % 1 == 0 else value


@register.filter
def getsubj(value, arg):
    return value.filter(subject__pk=arg)


@register.filter
def getbimester(value, arg):
    try:
        return value.get(bimester=arg).get_value_display()
    except:
        return ""
