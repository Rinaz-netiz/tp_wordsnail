from django.shortcuts import render
from .models import Raiting


__all__ = (
    "home",
    "raiting",
)


def home(request):
    return render(request, "wordsnail/home.html")


def raiting(request):
    raiting = Raiting.objects.all().order_by("-raiting")
    return render(request, "wordsnail/raiting.html", {"r": raiting})

