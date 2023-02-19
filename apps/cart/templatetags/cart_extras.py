from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.simple_tag
def get_promo_total_price(total_price, discount):
    return intcomma(total_price - (total_price // 100 * discount))
