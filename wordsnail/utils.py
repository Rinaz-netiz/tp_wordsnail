import json

from django.contrib.auth import login
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

from wordsnail.models import Shop, User, Profile
from wordsnail.forms import RegisterUserForm


def buy_item_in_shop(user, skin, price):
    """Функция добавляет юзеру скин"""
    try:
        user = User.objects.get(id=user.id)
    except ObjectDoesNotExist:
        return {"code": 500, "details": "Couldn't get data"}

    price = int(price)
    user_profile = user.profile
    if user_profile.money >= price:
        user_profile.money -= price
        user_profile.arr_skins.add(int(skin))
        user_profile.save()

    return {"code": 200, "details": "the operation was successful"}


def change_skin(current_user_id, id_picture):
    """Смена текущего скина"""
    try:
        user = User.objects.get(id=current_user_id)
    except ObjectDoesNotExist:
        return {"code": 500, "details": "objects is None"}

    user_profile = user.profile
    user_profile.current_skin = Shop.objects.get(id=id_picture).picture
    user_profile.save()

    return {"code": 200, "details": "Skin changed"}


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
        return {"code": 1,
                "things_in_shop": things_in_shop,
                "user_id": -1,
                "id_lis": [],
                "money": 0,
                "skin": 0}

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


def process_post_request(request):
    if not user_is_authenticated(request):
        return {"code": 401, "details": "User doesn't authorization"}, None

    if request.method == 'POST':
        data = json.loads(request.body)
        return None, data
    else:
        return {"code": 400, "details": "Don't post request"}, None


def action_with_skins(user, data):
    act = data.get("act")

    response = {"code": 400, "details": "data is None"}

    if act is None:
        return response

    if act == "buy":
        response = buy_item_in_shop(user, data.get("id"), data.get("price"))
    elif act == "will_apply":
        response = change_skin(user.id, int(data.get("id")))

    return response
