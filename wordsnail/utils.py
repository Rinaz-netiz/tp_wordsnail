from django.contrib.auth import login
from django.shortcuts import redirect

from wordsnail.models import Shop, User
from wordsnail.forms import RegisterUserForm


def add_skin(id_picture, current_user_id):
    """Функция добавляет юзеру скин"""
    skin = Shop.objects.get(id = id_picture)
    user = User.objects.get(id = current_user_id)
    user_profile = user.profile
    if user_profile.money >= skin.price:
        user_profile.money -= skin.price
        user_profile.arr_skins.add(skin)
        user_profile.save()


def change_skin(id_picture, current_user_id):
    """Смена текущего скина"""
    user = User.objects.get(id=current_user_id)
    user_profile = user.profile
    user_profile.current_skin = Shop.objects.get(id = id_picture).picture
    user_profile.save()


def getinfo(request):
    things_in_shop = Shop.objects.all()
    user = request.user
    if not user.is_authenticated:
        return redirect('index')
    current_user_id = user.id
    user_profile = user.profile
    id_lis = [el.id for el in user_profile.arr_skins.all()]
    return things_in_shop, current_user_id, id_lis, user_profile


def register_new_user(request):
    """Register new users"""
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)


