from django.urls import path
from .views import WishlistListView, wishlist_add

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistListView.as_view(), name='wishlist'),
    path('add/<int:product_id>', wishlist_add, name='wishlist_add'),
    ]
