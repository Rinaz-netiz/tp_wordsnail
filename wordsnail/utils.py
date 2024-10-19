from django.contrib.auth import login
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured

from wordsnail.models import Shop, User, Profile
from wordsnail.forms import RegisterUserForm


def add_skin(id_picture, current_user_id):
    """Функция добавляет юзеру скин"""
    skin = Shop.objects.get(id=id_picture)
    user = User.objects.get(id=current_user_id)
    user_profile = user.profile
    if user_profile.money >= skin.price:
        user_profile.money -= skin.price
        user_profile.arr_skins.add(skin)
        user_profile.save()


def change_skin(id_picture, current_user_id):
    """Смена текущего скина"""
    user = User.objects.get(id=current_user_id)
    user_profile = user.profile
    user_profile.current_skin = Shop.objects.get(id=id_picture).picture
    user_profile.save()


def getinfo(user):
    things_in_shop = Shop.objects.all()
    current_user_id = user.id
    user_profile = user.profile
    id_lis = [el.id for el in user_profile.arr_skins.all()]
    return things_in_shop, current_user_id, id_lis, user_profile


def postrequest(request, id_lis, current_user_id):
    id_picture = int(request.POST.get('act'))
    if id_picture in id_lis:
        change_skin(id_picture, current_user_id)
    else:
        add_skin(id_picture, current_user_id)
    return redirect('shop')


def register_new_user(request):
    """Register new users"""
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)


def user_is_authenticated(request):
    return request.user.is_authenticated


def balance_replenishment(user, money):
    if not money:
        return {"Code": 400, "details": "Money is empty"}

    try:
        user = User.objects.get(id=user.id).profile
    except ImproperlyConfigured:
        return {"Code": 500, "details": "ImproperlyConfigured"}

    user.money += int(money)
    user.save()

    return {"Code": 200, "details": "All ok"}


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

    print(data)
    return data
