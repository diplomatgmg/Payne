from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, UserCreateView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]
