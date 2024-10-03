from django.shortcuts import render


__all__ = (
    "home",
    "shop"
)


def home(request):
    return render(request, "wordsnail/home.html")


def shop(request):
    return render(request, "wordsnail/shop.html")
