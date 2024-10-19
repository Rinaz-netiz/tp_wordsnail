from django.urls import path, include
from django.contrib.auth import views as auth_views


from .views import *

urlpatterns = [
    path("register/", register, name='register'),
    path("rating/", raiting, name="rating"),
    path("shop/", shop, name="shop"),
    path("entry/", include('django.contrib.auth.urls')),
    path("", home, name="index"),
]