# In charts_filters.py

from django import template

register = template.Library()

@register.filter
def get_chart_labels(data):
    try:
        return [item['week'] for item in data]
    except (KeyError, TypeError):
        return []

@register.filter
def get_chart_data(data):
    try:
        return [item['total'] for item in data]
    except (KeyError, TypeError):
        return []
