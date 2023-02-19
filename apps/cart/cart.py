import random

from django.core.cache import cache

from .models import Cart as CartModel, CartItem as CartItemModel


class Cart:
    def __init__(self, request):
        if request.user.is_authenticated:
            cart, created = CartModel.objects.get_or_create(user_id_or_session_key=request.user.id)
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart, created = CartModel.objects.get_or_create(user_id_or_session_key=cart_id)
            else:
                cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.cartitem_set.all():
            yield item

    def __len__(self):
        return len(self.cart.cartitem_set.all())

    @staticmethod
    def new(request):
        random_user_id = random.randint(10 ** 15, 10 ** 16)
        cart = CartModel.objects.create(user_id_or_session_key=random_user_id)
        request.session['cart_id'] = cart.id
        return cart

    def add(self, product_id, quantity=1):
        cart_item, created = CartItemModel.objects.get_or_create(cart_id=self.cart.id, product_id=product_id)

        if cart_item:
            max_quantity = cart_item.product.quantity
            if quantity > max_quantity:
                quantity = max_quantity
            cart_item.quantity = quantity
            cart_item.save()

    def remove(self, product_id):
        cart_item = CartItemModel.objects.filter(cart_id=self.cart.id, product_id=product_id)
        if cart_item.exists():
            cart_item.delete()

    def clear(self):
        self.cart.cartitem_set.all().delete()

    # кэширование для корзины из корзины в header
    def total_price(self):
        cart_price = cache.get('cart_price')
        if not cart_price:
            cart_price = sum(cart_item.product.price * cart_item.quantity for cart_item in self)
            cache.set('cart_price', cart_price, 1)
        return cart_price
