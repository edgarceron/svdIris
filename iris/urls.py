"""Urls for users app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('check_iris', views.check_iris, name='check_iris'),
    path('check_iris2', views.check_iris2, name='check_iris2'),
    path('upload/', webservices.ImageViewSet.as_view(), name='upload'),
    path('upload2/', webservices.ImageViewSet2.as_view(), name='upload2'),
]