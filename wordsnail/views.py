from django.shortcuts import render


__all__ = (
    "home",
    "register",
    "login"
)


def home(request):
    return render(request, "wordsnail/home.html")


def register(request):
    return render(request, "wordsnail/register.html")


def login(request):
    return render(request, "wordsnail/login.html")




