from django.urls import path

from .views import *

urlpatterns = [
    path('whoami/', whoami),
    path('source_code/', source_code),
]
