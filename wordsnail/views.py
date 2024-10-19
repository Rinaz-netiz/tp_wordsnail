import random
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from wordsnail.forms import RegisterUserForm
from wordsnail.utils import (register_new_user, order_by_rating,
                             getinfo, postrequest,
                             balance_replenishment, user_is_authenticated)
from wordsnail.words_for_game import WORDS


__all__ = (
    "home",
    "register",
    "raiting",
    "shop",
    "play",
    "get_random_word",
    "put_cash",
    "loginhome"
)


def home(request):
    return render(request, "wordsnail/home.html")


def loginhome(request):
    return render(request, "wordsnail/loginhome.html")


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
    data = order_by_rating(request)

    return render(request, 'wordsnail/rating.html', data)


def shop(request):  # страница магазина
    if not user_is_authenticated(request):
        return redirect('index')

    things_in_shop, current_user_id, id_lis, user_profile = getinfo(request.user)
    if request.method == 'POST':
        return postrequest(request, id_lis, current_user_id)

    return render(request, "wordsnail/shop.html", {"things_in_shop" : things_in_shop,
                                                   "user_id": current_user_id,
                                                   "id_lis": id_lis,
                                                   "money": user_profile.money,
                                                   "skin": user_profile.current_skin})


def play(request):
    return render(request, "wordsnail/game_page.html")


def get_random_word(request):
    word = random.choice(WORDS)
    return JsonResponse({"word": word, "len": len(word)})


@csrf_exempt  # Это отключает проверку CSRF. Используй только в тестовых целях, в продакшене лучше настроить CSRF корректно.
def put_cash(request):
    if not user_is_authenticated(request):
        return redirect("play")

    if request.method == 'POST':
        data = json.loads(request.body)  # Получаем данные из запроса

        response = balance_replenishment(request.user, data.get("money"))
    else:
        response = {"Code": 400, "details": "Don't post request"}

    return JsonResponse(response)


