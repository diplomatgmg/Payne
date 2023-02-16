from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import UsernameValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
            _('имя пользователя'),
            max_length=32,
            unique=True,
            validators=(UsernameValidator(),),
            error_messages={
                "unique": _('Пользователь с таким именем уже существует.'),
                },
            )

    first_name = models.CharField(_('имя'), max_length=16, blank=True)
    last_name = models.CharField(_('фамилия'), max_length=16, blank=True)
    email = models.EmailField(
            _('почта'),
            blank=True,
            unique=True,
            error_messages={
                "unique": _('Пользователь с такой почтой уже существует.'),
                },
            )

    image = models.ImageField(_('аватарка'), upload_to='user_images', blank=True)

    about_me = models.CharField(_('кратко о себе'), blank=True, max_length=128)
    phone = models.CharField(_('телефон'), max_length=16, blank=True)
    city = models.CharField(_('город'), max_length=32, blank=True)
    street = models.CharField(_('улица'), max_length=64, blank=True)
    house = models.CharField(_('дом'), max_length=16, blank=True)
    building = models.CharField(_('корпус'), max_length=16, blank=True)
    apartment = models.CharField(_('квартира'), max_length=16, blank=True)

    comments = models.PositiveIntegerField(_('комментариев'), default=0, editable=False,
                                           help_text=_('Количество комментариев'
                                                       'под постами пользователя'))

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
            _("персонал"),
            default=False,
            help_text=_("пользователь является частью персонала"),
            )
    is_verified = models.BooleanField(
            _("подтверждена почта"),
            default=False,
            )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("пользователь")
        verbose_name_plural = _("пользователи")

    @staticmethod
    def find_user(username_or_email, password):
        user = CustomUser.objects.filter(username=username_or_email).last() \
               or CustomUser.objects.filter(email=username_or_email).last()
        return user if user and check_password(password, user.password) else False

    def __str__(self):
        return self.username
