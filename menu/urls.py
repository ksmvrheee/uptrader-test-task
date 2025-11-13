from django.urls import path

from .views import *


urlpatterns = [
    path('example/', show_menu_example)
]
