from django.shortcuts import render
from wordsnail.models import *

__all__ = (
    "home",
    "shop"
)



def home(request):
    return render(request, "wordsnail/home.html")


def shop(request):
    lis = Shop.objects.all()

    current_user_id = 2  # временный айди пользователя(пока нет таблицы пользователей)
    current_money = 2100  # временые деньги (в таблиеце пользователей должно быт поле для денег)


    buy_yet = Purchased.objects.filter(user_id = current_user_id)
    id_lis = [el.things_id.id for el in buy_yet]  # список id вещей, которые уже купил user

    return render(request, "wordsnail/shop.html", {"things_in_shop" : lis,
                                                   "user_id": current_user_id,
                                                   "id_lis": id_lis,
                                                   "money": current_money,})


