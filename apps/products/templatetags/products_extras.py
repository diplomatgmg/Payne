from django import template


register = template.Library()


@register.filter
def get_color_rating(value: float):
    if 4 <= value <= 5:
        return '#00FF24'
    elif 3 <= value <= 4:
        return '#ffb700'
    elif 2 <= value <= 4:
        return '#FF6000'
    elif 0 <= value <= 2:
        return '#ff0000'