# urls.py
from django.urls import path
from .views import create_metadata

urlpatterns = [
    path('create-metadata/', create_metadata, name='create_metadata'),
]
