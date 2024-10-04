from django.shortcuts import render
from wordsnail.models import Shop

__all__ = (
    "home",
    "shop"
)



def home(request):
    return render(request, "wordsnail/home.html")


def shop(request):
    lis = Shop.objects.all()
    return render(request, "wordsnail/shop.html", {"ls" : lis})


