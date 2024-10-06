from traceback import print_tb


from django.shortcuts import render, redirect
from wordsnail.models import Users, Shop
from .utils import add_skin, change_skin

__all__ = (
    "home",
    "shop"
)

'''Временные переменные для теста'''
current_user_id = 3  # временный айди пользователя


def home(request):
    return render(request, "wordsnail/home.html")


def shop(request):  # страница магазина
    things_in_shop = Shop.objects.all()
    user = Users.objects.get(id = current_user_id)
    id_lis = [el.id for el in user.arr_skins.all()]

    if request.method == 'POST':
        id_picture = int(request.POST.get('act'))
        if id_picture in id_lis:
            change_skin(id_picture, current_user_id)
        else:
            add_skin(id_picture, current_user_id)
        return redirect('shop')

    return render(request, "wordsnail/shop.html", {"things_in_shop" : things_in_shop,
                                                   "user_id": current_user_id,
                                                   "id_lis": id_lis,
                                                   "money": user.money,
                                                   "skin": user.current_skin})


