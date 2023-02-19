from django import template
from django.core.cache import cache

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


@register.simple_tag
def parse_url(request, **kwargs):
    page = kwargs.get('page')
    if not page:
        page = request.GET.get('page', 1)

    ordering = kwargs.get('ordering')
    if not ordering:
        ordering = request.GET.get('ordering', '-rating')

    search = kwargs.get('search')
    if not search:
        search = request.GET.get('search', '')

    url = f'?page=%s&ordering=%s&search=%s' % (page, ordering, search)

    return url
