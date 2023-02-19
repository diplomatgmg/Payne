from django.urls import path

from .views import ShopView, ShopProductView

app_name = 'shop'

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('<int:pk>/', ShopProductView.as_view(), name='product-detail')
]
