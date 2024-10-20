from django.contrib.auth import login
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

from wordsnail.models import Shop, User, Profile
from wordsnail.forms import RegisterUserForm


def add_skin(id_picture, current_user_id):
    """Функция добавляет юзеру скин"""
    try:
        skin = Shop.objects.get(id=id_picture)
        user = User.objects.get(id=current_user_id)
    except ObjectDoesNotExist:
        return

    user_profile = user.profile
    if user_profile.money >= skin.price:
        user_profile.money -= skin.price
        user_profile.arr_skins.add(skin)
        user_profile.save()


def change_skin(id_picture, current_user_id):
    """Смена текущего скина"""
    try:
        user = User.objects.get(id=current_user_id)
    except ObjectDoesNotExist:
        return

    user_profile = user.profile
    user_profile.current_skin = Shop.objects.get(id=id_picture).picture
    user_profile.save()


def getinfo(request):
    try:
        things_in_shop = Shop.objects.all()
    except ObjectDoesNotExist:
        return {"code": -1,
                "things_in_shop": [],
                "user_id": 0,
                "id_lis": [],
                "money": -1,
                "skin": ""}
    if not user_is_authenticated(request):
        return {"code": 0,
                "things_in_shop": things_in_shop,
                "user_id": -1,
                "id_lis": [],
                "money": -1,
                "skin": ""}

    user = request.user
    current_user_id = user.id
    user_profile = user.profile
    id_lis = [el.id for el in user_profile.arr_skins.all()]
    return {"code": 1,
            "things_in_shop": things_in_shop,
            "user_id": current_user_id,
            "id_lis": id_lis,
            "money": user_profile.money,
            "skin": user_profile.current_skin}


def postrequest(request, id_lis, current_user_id):
    id_picture = int(request.POST.get('act'))
    if id_picture in id_lis:
        change_skin(id_picture, current_user_id)
    else:
        add_skin(id_picture, current_user_id)



def register_new_user(request):
    """Register new users"""
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)


def user_is_authenticated(request):
    return request.user.is_authenticated


def balance_replenishment_and_change_rating(user, money, rating):
    if money is None:
        return {"code": 400, "details": "Money is empty"}
    if rating is None:
        return {"code": 400, "details": "Rating is empty"}

    try:
        user = User.objects.get(id=user.id).profile
    except ImproperlyConfigured:
        return {"code": 500, "details": "ImproperlyConfigured"}

    user.money += int(money)
    user.rating += int(rating)
    user.save()

    return {"code": 200, "details": "All ok"}


def order_by_rating(request):
    data = {'r': [],
            'current_user_rating': 0,
            'user_place': 0}

    try:
        all_ratings = Profile.objects.all().order_by('-rating')
    except ImproperlyConfigured:
        return data

    for index, user in enumerate(all_ratings, start=1):
        try:
            data["r"].append({"place": index, "name": User.objects.get(id=user.id).username, "rating": user.rating})

            if user_is_authenticated and user.id == request.user.id:
                data["current_user_rating"] = user.rating
                data["user_place"] = index
        except ImproperlyConfigured:
            pass

    return data
