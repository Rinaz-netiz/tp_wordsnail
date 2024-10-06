from .models import Shop, Users


def add_skin(id_picture, current_user_id):
    '''Функция добавляет юзеру скин'''
    skin = Shop.objects.get(id = id_picture)
    user = Users.objects.get(id = current_user_id)
    if user.money >= skin.price:
        user.money -= skin.price
        user.arr_skins.add(skin)
        user.save()


def change_skin(id_picture, current_user_id):
    '''Смена текущего скина'''
    user = Users.objects.get(id=current_user_id)
    user.current_skin = Shop.objects.get(id = id_picture).picture
    user.save()
