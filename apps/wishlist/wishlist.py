import random

from .models import Wishlist as WishlistModel, WishlistItem as WishlistItemModel


class Wishlist:
    def __init__(self, request):
        if request.user.is_authenticated:
            wishlist, created = WishlistModel.objects.get_or_create(user_id_or_session_key=request.user.id)
        else:
            wishlist_id = request.session.get('cart_id')
            if wishlist_id:
                wishlist, created = WishlistModel.objects.get_or_create(user_id_or_session_key=wishlist_id)
            else:
                wishlist = self.new(request)
        self.wishlist = wishlist

    def __iter__(self):
        for item in self.wishlist.wishlistitem_set.all():
            yield item

    def __len__(self):
        return len(self.wishlist.wishlistitem_set.all())

    @staticmethod
    def new(request):
        random_user_id = random.randint(10 ** 15, 10 ** 16)
        wishlist = WishlistModel.objects.create(user_id_or_session_key=random_user_id)
        request.session['wishlist_id'] = wishlist.id
        return wishlist

    def add(self, product_id):
        WishlistItemModel.objects.get_or_create(wishlist_id=self.wishlist.id, product_id=product_id)

    def remove(self, product_id):
        cart_item = WishlistItemModel.objects.filter(cart_id=self.wishlist.id, product_id=product_id)
        if cart_item.exists():
            cart_item.delete()

    def clear(self):
        self.wishlist.cartitem_set.all().delete()
