from django.urls import path, include


from .views import *

urlpatterns = [
    path("register/", register, name='register'),
    path("rating/", rating, name="rating"),
    path("shop/", shop, name="shop"),
    path("play/", play, name="play"),
    path("entry/", include('django.contrib.auth.urls')),
    path('shop/api/buy-item/', buy_item, name='buy_item'),
    path('api/random-word/', get_random_word, name='random_word'),
    path('api/put-cash/', put_cash, name='put_cash'),
    path("", home, name="index"),
]