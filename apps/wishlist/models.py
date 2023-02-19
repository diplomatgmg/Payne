from django.db import models
from django.utils import timezone

from apps.products.models import Product
from apps.users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class Wishlist(models.Model):
    user_id_or_session_key = models.CharField(verbose_name=_('привязка к сессии или пользователю'),
                                              unique=True,
                                              max_length=128)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('корзина')
        verbose_name_plural = _('корзины')

    def __str__(self):
        user_or_session = self.user_id_or_session_key
        try:
            user_or_session = CustomUser.objects.get(id=user_or_session)
            return f'Корзина пользователя {user_or_session}'
        except:
            return f'Корзина неавторизованного пользователя {user_or_session}'


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(to=Wishlist, on_delete=models.CASCADE, verbose_name=_('корзина'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('товар'))

    timestamp = models.DateTimeField(_('последнее изменение'), auto_now_add=True)

    class Meta:
        verbose_name = _('предмет из избранного')
        verbose_name_plural = _('предметы из избранного')

    def __str__(self):
        return self.product.name
