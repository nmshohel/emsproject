from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('userprofile', user_profile, name='user_profile'),
]
