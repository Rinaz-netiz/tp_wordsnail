from django.urls import path, include
from django.contrib.auth import views as auth_views


from .views import *

urlpatterns = [
    path("", home, name="index"),
    path('register/', register, name='register'),
    path('', include('django.contrib.auth.urls')),
]