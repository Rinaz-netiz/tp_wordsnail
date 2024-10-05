from traceback import print_tb


from django.shortcuts import render, redirect
from wordsnail.models import *

__all__ = (
    "home",
    "shop"
)

'''Временные переменные для теста (пока нет таблицы пользователей)'''
current_user_id = 1  # временный айди пользователя
current_money = 2100  # временые деньги


def home(request):
    return render(request, "wordsnail/home.html")


def shop(request):  # страница магазина
    things_in_shop = Shop.objects.all()  # все вещи из магазина
    buy_yet = Purchased.objects.filter(user_id = current_user_id)
    id_lis = [el.things_id.id for el in buy_yet]  # список id вещей, которые уже купил user

    if request.method == 'POST':
        add_things(request.POST, id_lis, things_in_shop)
        return redirect('shop')

    return render(request, "wordsnail/shop.html", {"things_in_shop" : things_in_shop,
                                                   "user_id": current_user_id,
                                                   "id_lis": id_lis,
                                                   "money": current_money,})


def add_things(mypost, id_lis, things_in_shop): # функция для покупки или смены вещи
    for el in things_in_shop:
        if str(el.id) in mypost:
            if el.id not in id_lis:  # покупка
                if current_money > el.price:
                    """Поменять количество денег в таблице Users"""
                    buy = Purchased()
                    buy.things_id = el
                    buy.user_id = current_user_id
                    buy.save()
            else: # меняем скин
                '''В моделе пользователей будет поле для хранения пути к теущему скиину'''
                pass




