import random
import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from wordsnail.forms import RegisterUserForm
from wordsnail.utils import (register_new_user, order_by_rating,
                             getinfo, postrequest,
                             balance_replenishment_and_change_rating,
                             user_is_authenticated)
from wordsnail.words_for_game import WORDS


__all__ = (
    "home",
    "register",
    "rating",
    "shop",
    "play",
    "get_random_word",
    "put_cash",
)


def home(request):
    return render(request, "wordsnail/home.html")


def register(request):
    if request.method == "POST":
        register_new_user(request)
        return redirect("play")

    messages.error(request, "Unsuccessful registration. Invalid information.")

    form = RegisterUserForm()
    return render(request, "registration/register.html", {'form': form})


def rating(request):
    data = order_by_rating(request)
    return render(request, 'wordsnail/rating.html', data)


def shop(request):  # страница магазина
    data = getinfo(request)
    if data["code"] == -1:
        return render(request, "wordsnail/shop.html")

    if request.method == 'POST':
        if user_is_authenticated(request):
            postrequest(request, data["id_lis"], data["user_id"])
            return redirect('shop')

        data["code"] = 2
        return render(request, "wordsnail/shop.html", data)

    return render(request, "wordsnail/shop.html", data)


def play(request):
    return render(request, "wordsnail/game_page.html")


def get_random_word(request):
    word = random.choice(WORDS)
    return JsonResponse({"word": word, "len": len(word)})


@csrf_exempt  # Это отключает проверку CSRF. Используй только в тестовых целях, в продакшене лучше настроить CSRF корректно.
def put_cash(request):
    if not user_is_authenticated(request):
        return JsonResponse({"code": 401, "details": "User doesn't authorization"})

    if request.method == 'POST':
        data = json.loads(request.body)  # Получаем данные из запроса
        response = balance_replenishment_and_change_rating(request.user, data.get("money"), data.get("rating"))
    else:
        response = {"code": 400, "details": "Don't post request"}

    return JsonResponse(response)


