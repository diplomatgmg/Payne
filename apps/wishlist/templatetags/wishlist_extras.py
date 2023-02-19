from django import template

register = template.Library()


@register.filter
def color_stock(quntity):
    if quntity < 3:
        return ['red', 'Очень мало']
    elif quntity < 7:
        return ['orange', 'Мало']
    elif quntity < 10:
        return ['green', 'В наличии']
    elif quntity >= 10:
        return ['blue', 'Много'
                ]
