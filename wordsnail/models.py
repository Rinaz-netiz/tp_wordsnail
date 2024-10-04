from optparse import make_option

from django.db import models

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


