from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from .wishlist import Wishlist


class WishlistListView(TemplateView):
    template_name = 'wishlist/wishlist.html'


def wishlist_add(request, product_id):
    cart = Wishlist(request)
    cart.add(product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))
