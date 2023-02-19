from .cart import Cart


def get_user_cart(request):
    user_cart = Cart(request)
    return {'user_cart': user_cart}

# def get_user_wishlist(request):
#     wishlist = None
#     if request.user.is_authenticated:
#         wishlist = WishlistItem.objects.filter(user=request.user)
#
#     return {'wishlist': wishlist}
