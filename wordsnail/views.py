from traceback import print_tb


from django.shortcuts import render, redirect
from wordsnail.models import *

__all__ = (
    "home",
    "shop"
)

'''Временные переменные для теста'''
current_user_id = 4  # временный айди пользователя


def home(request):
    return render(request, "wordsnail/home.html")


def shop(request):  # страница магазина
    things_in_shop = Shop.objects.all()  # все вещи из магазина
    buy_yet = Purchased.objects.filter(user_id = current_user_id)
    id_lis = [el.things_id.id for el in buy_yet]  # список id вещей, которые уже купил user
    user = Users.objects.filter(id = current_user_id).first()

    if request.method == 'POST':
        add_things(request.POST, id_lis, things_in_shop, user)
        return redirect('shop')

    return render(request, "wordsnail/shop.html", {"things_in_shop" : things_in_shop,
                                                   "user_id": current_user_id,
                                                   "id_lis": id_lis,
                                                   "money": user.money,
                                                   "skin": user.currentskin})


def add_things(mypost, id_lis, things_in_shop, user): # функция для покупки или смены вещи
    for el in things_in_shop:
        if str(el.id) in mypost:
            if el.id not in id_lis:  # покупка
                if user.money >= el.price:
                    user.money -= el.price
                    buy = Purchased()
                    buy.things_id = el
                    buy.user_id = user
                    buy.save()
            else: # меняем скин
                user.currentskin = things_in_shop.filter(id = el.id).first().picture
            user.save()



