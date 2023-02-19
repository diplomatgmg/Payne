from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product
from apps.users.models import CustomUser


class Cart(models.Model):
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


class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, verbose_name=_('корзина'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    quantity = models.PositiveIntegerField(_('количество'), default=1)
    updated = models.DateTimeField(_('создана'), auto_now=True)
    timestamp = models.DateTimeField(_('последнее изменение'), auto_now_add=True)

    class Meta:
        verbose_name = _('предмет из корзины')
        verbose_name_plural = _('предметы из корзины')

    def product_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name


class PromoCodeExpiredException(Exception):
    pass


class PromoCode(models.Model):
    promo_code = models.CharField(_('промокод'), max_length=64, unique=True)
    discount = models.PositiveSmallIntegerField(_('скидка %'))
    activations_left = models.PositiveIntegerField(_('количество активаций'))
    creation_date = models.DateTimeField(_('создан'), default=timezone.now)
    time_left = models.DurationField(_('длительность'), default=timezone.timedelta(days=1),
                                     help_text=_('Дней часов:минут:секунд'))
    active = models.BooleanField(_('активен'), default=True)

    class Meta:
        verbose_name = _('промокод')
        verbose_name_plural = _('промокоды')

    def save(self, *args, **kwargs):
        if (self.activations_left == 0) or (timezone.now() > self.time_left + self.creation_date):
            self.active = False
        super().save(*args, **kwargs)

    def use_promo(self):
        if self.time_left > timezone.now():
            self.activations_left -= 1
            self.save()
        else:
            raise PromoCodeExpiredException

    def valid(self):
        return self.active

    def add_promo_in_session(self, request):
        request.session['promo_code'] = self.promo_code
        request.session['promo_discount'] = self.discount
