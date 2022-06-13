from lib2to3.pgen2 import token
from django.contrib import admin
from django.urls import path

from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('login', login_attempt, name="login"),
    path('register/', register_attempt, name="register"),
    path('token/', token_send, name="token_send"),
    path('success/', success, name="success"),
]
