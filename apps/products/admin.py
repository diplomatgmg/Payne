from django.contrib import admin

from .models import Brand, Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ('category',)
    list_display = ('category',)
    search_fields = ('category',)


@admin.register(Brand)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price', 'real_price', 'discount', 'rating', 'quantity', 'category')
    fields = ('brand', 'category', 'name', 'description', 'image', 'rating',
              ('quantity', 'count_sales'), 'added_at', ('real_price', 'price', 'discount'))
    search_fields = ('name', 'brand__name')
    ordering = ('-name',)
    readonly_fields = ('count_sales', 'price')
