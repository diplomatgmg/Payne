from .wishlist import Wishlist


def get_user_wishlist(request):
    user_wishlist = Wishlist(request)
    return {'user_wishlist': user_wishlist}
