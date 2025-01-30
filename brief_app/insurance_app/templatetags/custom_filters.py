import json
from django import template

register = template.Library()

@register.filter
def jsonify(value):
    return json.dumps(value)



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)