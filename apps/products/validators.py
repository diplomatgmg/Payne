from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError




def validate_discount(discount):
    if discount > 90:
        raise ValidationError(
                _('%(discount)s не может быть больше 90%'),
                params={
                    'discount': discount
                    },
                )