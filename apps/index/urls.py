from django.contrib import admin
from django.urls import include, path

from .views import IndexTemplateView

app_name = 'index'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    ]
