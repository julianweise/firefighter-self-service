from django.template.defaulttags import register
from django.utils.translation import gettext


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_obj_attr(obj, attr):
    return getattr(obj, attr)


@register.filter
def call_obj_func(obj, attr):
    return getattr(obj, attr)()


@register.filter(name='template_trans')
def template_trans(text):
    try:
        return gettext(text)
    except:
        return text
