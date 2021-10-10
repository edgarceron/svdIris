"""Urls for users app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('check_iris', views.check_iris, name='check_iris'),
    path('upload/', webservices.ImageViewSet.as_view(), name='upload'),
]