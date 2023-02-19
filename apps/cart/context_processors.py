from .cart import Cart


def get_user_cart(request):
    user_cart = Cart(request)
    return {'user_cart': user_cart}
