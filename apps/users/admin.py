from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = (('username', 'password'), ('first_name', 'last_name'), ('email', 'is_verified'), 'image',
              'comments', 'about_me', 'phone', 'city', 'street', 'house', 'building', 'apartment',
              ('date_joined', 'last_login'), ('is_staff', 'is_superuser'), 'groups', 'user_permissions')
    list_display = ('username', 'email')

    readonly_fields = ('username', 'password', 'comments')
    filter_horizontal = ('groups', 'user_permissions',)
