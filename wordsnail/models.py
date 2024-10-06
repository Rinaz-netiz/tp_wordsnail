from optparse import make_option

from django.db import models
from django.template.defaultfilters import default


class Shop(models.Model):
    picture = models.ImageField(upload_to="shopThings/gifs/")
    title = models.CharField(unique=True, max_length=20)
    price = models.IntegerField()


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    current_skin = models.ImageField(upload_to="shopThings/gifs/", default="shopThings/gifs/6152297562.jpg")  # test
    money = models.IntegerField(default=2100)
    arr_skins = models.ManyToManyField(Shop)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'