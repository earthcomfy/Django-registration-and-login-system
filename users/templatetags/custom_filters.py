from django import template

register = template.Library()

@register.filter
def get_sale_commission(monthly_totals, month):
    for entry in monthly_totals:
        if entry['month'].month == month.month:
            return entry['commission']
    return 0.00
