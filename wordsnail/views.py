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
                             user_is_authenticated, buy_item_in_shop,
                             process_post_request, action_with_skins)
from wordsnail.words_for_game import WORDS


__all__ = (
    "home",
    "register",
    "rating",
    "shop",
    "play",
    "get_random_word",
    "put_cash",
    "buy_item",
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


def shop(request):
    """Отображение страницы магазина."""
    data = getinfo(request)

    if data["code"] == -1:
        return render(request, "wordsnail/shop.html")

    return render(request, "wordsnail/shop.html", data)


@csrf_exempt
def buy_item(request):
    error_response, data = process_post_request(request)
    if error_response:
        return JsonResponse(error_response)

    response = action_with_skins(request.user, data)
    return JsonResponse(response)


def play(request):
    return render(request, "wordsnail/game_page.html")


def get_random_word(request):
    word = random.choice(WORDS)
    return JsonResponse({"word": word, "len": len(word)})


@csrf_exempt  # Это отключает проверку CSRF. Используй только в тестовых целях, в продакшене лучше настроить CSRF корректно.
def put_cash(request):
    error_response, data = process_post_request(request)
    if error_response:
        return JsonResponse(error_response)

    response = balance_replenishment_and_change_rating(request.user, data.get("money"), data.get("rating"))
    return JsonResponse(response)


