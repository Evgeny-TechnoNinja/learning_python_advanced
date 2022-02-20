from django.urls import path

from .views import *

urlpatterns = [
    path('', random_sequence),
]
