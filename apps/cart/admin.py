from django.contrib import admin

from .models import CartItem, Cart, PromoCode


class CartItemInline(admin.TabularInline):
    extra = 1
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline,)


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    fields = ('promo_code', 'discount', 'activations_left', 'time_left', 'active')
    list_display = ('promo_code', 'discount', 'activations_left', 'creation_date', 'time_left', 'active')