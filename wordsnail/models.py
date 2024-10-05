from optparse import make_option

from django.db import models
from django.template.defaultfilters import default


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    currentskin = models.ImageField(upload_to="shopThings/gifs/", default="shopThings/gifs/6152297562.jpg")  # test
    money = models.IntegerField(default=2100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'


class Shop(models.Model):

    id = models.IntegerField(primary_key=True)
    picture = models.ImageField(upload_to="shopThings/gifs/")
    name = models.CharField(default="name", max_length=20)
    price = models.IntegerField(default=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class Purchased(models.Model): # купленные вещи
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE) # Внешний ключ на таблицу с юзерами
    things_id = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Purchased'
        verbose_name_plural = 'Purchaseds'

