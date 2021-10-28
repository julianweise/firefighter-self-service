from django.template.defaulttags import register


@register.filter(name='replace_whitespace')
def replace_whitespace(value):
    return value.replace(" ", "_")
