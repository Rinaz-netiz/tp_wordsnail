from django.shortcuts import render, redirect
from django.contrib import messages

from wordsnail.models import Users, Shop, Raiting
from wordsnail.utils import add_skin, change_skin, register_new_user
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
    raiting = Raiting.objects.all().order_by("-raiting")
    return render(request, "wordsnail/raiting.html", {"r": raiting})


def shop(request):  # страница магазина
    ...
    # things_in_shop = Shop.objects.all()
    # user = Users.objects.get(id = current_user_id)
    # id_lis = [el.id for el in user.arr_skins.all()]
    #
    # if request.method == 'POST':
    #     id_picture = int(request.POST.get('act'))
    #     if id_picture in id_lis:
    #         change_skin(id_picture, current_user_id)
    #     else:
    #         add_skin(id_picture, current_user_id)
    #     return redirect('shop')
    #
    # return render(request, "wordsnail/shop.html", {"things_in_shop" : things_in_shop,
    #                                                "user_id": current_user_id,
    #                                                "id_lis": id_lis,
    #                                                "money": user.money,
    #                                                "skin": user.current_skin})
    #

