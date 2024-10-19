from django.shortcuts import render, redirect
from django.contrib import messages

from wordsnail.models import Shop, Rating
from wordsnail.utils import register_new_user, change_skin, add_skin, getinfo, postrequest
from wordsnail.forms import RegisterUserForm


__all__ = (
    "home",
    "register",
    "raiting",
    "shop",
)

def home(request):
    return render(request, "wordsnail/home.html")


def register(request):
    if request.method == "POST":
        register_new_user(request)
        messages.success(request, "Registration successful.")
        redirect("index")
    else:
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = RegisterUserForm()
    return render(request, "registration/register.html", {'form': form})


def raiting(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('index')
    rating = Rating.objects.all().order_by("-rating")
    return render(request, "wordsnail/raiting.html", {"r": rating, 'user': user})


def shop(request):  # страница магазина
    user = request.user
    if not user.is_authenticated:
        return redirect('index')

    things_in_shop, current_user_id, id_lis, user_profile = getinfo(user)
    if request.method == 'POST':
        return postrequest(request, id_lis, current_user_id)

    return render(request, "wordsnail/shop.html", {"things_in_shop" : things_in_shop,
                                                   "user_id": current_user_id,
                                                   "id_lis": id_lis,
                                                   "money": user_profile.money,
                                                   "skin": user_profile.current_skin})


