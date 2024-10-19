import random

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from wordsnail.models import Shop, Raiting, User
from wordsnail.utils import register_new_user, change_skin, add_skin, getinfo, postrequest
from wordsnail.forms import RegisterUserForm


__all__ = (
    "home",
    "register",
    "raiting",
    "shop",
    "play",
    "get_random_word",
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
    raiting = Raiting.objects.all().order_by("-raiting")
    return render(request, "wordsnail/raiting.html", {"r": raiting})


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


def play(request):
    return render(request, "wordsnail/game_page.html")


WORDS = ["груша", "банан", "слива", "персик"]


def get_random_word(request):
    word = random.choice(WORDS)
    return JsonResponse({"word": word, "len": len(word)})

