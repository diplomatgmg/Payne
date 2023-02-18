from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, UserCreateView, ProfileView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('profile/<int:pk>/', ProfileView.as_view(), name='profile')
    ]
