import random

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_random_rating():
    r_num = random.randint(0, 10)
    if r_num == 0:
        return round(random.uniform(1, 2), 1)
    if r_num == 1:
        return round(random.uniform(2, 3), 1)
    if 2 <= r_num <= 3:
        return round(random.uniform(3, 4), 1)
    if 4 <= r_num <= 6:
        return round(random.uniform(4, 4.7), 1)
    if 7 <= r_num <= 10:
        return round(random.uniform(4.5, 5), 1)


def validate_discount(discount):
    if discount > 90:
        raise ValidationError(
                _('%(discount)s не может быть больше 90%'),
                params={
                    'discount': discount
                    },
                )


class ProductCategory(models.Model):
    category = models.CharField(verbose_name=_('категория'),
                                max_length=32,
                                blank=False,
                                null=False)

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')

    def __str__(self):
        return self.category


class Brand(models.Model):
    name = models.CharField(verbose_name=_('название бренда'),
                            max_length=32,
                            unique=True,
                            blank=False,
                            null=False)

    class Meta:
        verbose_name = _('бренд')
        verbose_name_plural = _('бренды')

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(verbose_name=_('бренд'),
                              to=Brand,
                              on_delete=models.CASCADE)

    category = models.ForeignKey(verbose_name=_('категория'),
                                 to=ProductCategory,
                                 on_delete=models.CASCADE)

    name = models.CharField(verbose_name=_('название'),
                            max_length=64,
                            blank=False,
                            null=False)

    description = models.TextField(verbose_name=_('описание'),
                                   max_length=1024,
                                   blank=False,
                                   null=False)

    image = models.ImageField(verbose_name=_('изображение'),
                              upload_to='product_images')

    price = models.PositiveIntegerField(verbose_name=_('цена со скидкой'),
                                        editable=False,
                                        help_text='цена товара со скидкой')

    real_price = models.PositiveIntegerField(verbose_name=_('реальная цена'),
                                             null=False,
                                             blank=False,
                                             help_text='цена товара')

    discount = models.PositiveSmallIntegerField(verbose_name=_('скидка (%)'),
                                                default=0,
                                                validators=(validate_discount,))

    rating = models.DecimalField(verbose_name=_('рейтинг (1-5)'),
                                 default=get_random_rating,
                                 max_digits=2,
                                 decimal_places=1)

    quantity = models.PositiveSmallIntegerField(verbose_name=_('в наличии шт.'),
                                                default=0)

    count_sales = models.PositiveIntegerField(verbose_name=_('продано'),
                                              default=0)

    added_at = models.DateField(verbose_name=_('поступило'),
                                default=timezone.now)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def save(self, *args, **kwargs):
        self.price = self.get_price_discount()
        super().save(*args, **kwargs)

    def get_price_discount(self):
        return self.real_price - (self.real_price // 100 * self.discount)

    def __str__(self):
        return f'{self.brand} {self.name}'
