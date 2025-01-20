from django import template
from itertools import groupby
register = template.Library()

@register.filter
def format_rupiah(value):
    try:
        value = int(value)
        return f"Rp {value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value


