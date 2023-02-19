from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.cart.cart import Cart
from apps.cart.models import PromoCode
from mixins.views import TitleMixin


# Create your views here.

class CartView(TitleMixin, TemplateView):
    title = 'Корзина'
    template_name = 'cart/cart.html'


def cart_add(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product_id, quantity)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def apply_promo(request):
    promo_code = request.POST.get('promo_code')
    promo_code_model = PromoCode.objects.filter(promo_code=promo_code).last()

    if promo_code_model and promo_code_model.valid():
        promo_code_model.add_promo_in_session(request)

    return redirect(request.META.get('HTTP_REFERER', '/'))
