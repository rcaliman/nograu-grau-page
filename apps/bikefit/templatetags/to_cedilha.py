from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def to_cedilha(value:str):
    return value.replace('c','ç')