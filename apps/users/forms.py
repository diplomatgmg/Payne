from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm, UserCreationForm

from .models import CustomUser


class UserLoginForm(AuthenticationForm):
    username_or_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}))

    class Meta:
        model = CustomUser
        fields = ('username_or_email', 'password')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form__input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form__input'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form__input'}))
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form__input'}))
    about_me = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form__input',
            'placeholder': 'Напишите пару слов о себе...',
        }))
    image = forms.ImageField(required=False)
    email = forms.CharField(required=False, widget=forms.EmailInput(attrs={'class': 'form__input'}))
    phone = forms.RegexField(required=False, regex=r'^[+]?\d{10,11}$', help_text='Формат: 7 999 999 99 99',
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form__input',
                                 }))

    street = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form__input'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form__input'}))
    house = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form__input'}))
    building = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form__input'}))
    apartment = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form__input'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'about_me', 'image', 'email',
                  'phone', 'city', 'street', 'house', 'building', 'apartment')


class UserChangePasswordForm(PasswordChangeForm):
    error_messages = {'password_incorrect': 'Пароль введен неправильно.',
                      'password_mismatch': 'Пароли не совпадают.', }
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input'}))

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')
