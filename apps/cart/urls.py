from django.urls import path

from .views import CartView, cart_add, cart_remove, cart_clear, apply_promo

app_name = 'cart'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/<int:product_id>', cart_add, name='cart_add'),
    path('remove/<int:product_id>', cart_remove, name='cart_remove'),
    path('clear/', cart_clear, name='cart_clear'),

    path('apply_promo/', apply_promo, name='apply_promo'),
]
