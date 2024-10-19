from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Shop(models.Model):
    picture = models.ImageField(upload_to="shopThings/gifs/")
    title = models.CharField(unique=True, max_length=20)
    price = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_skin = models.ImageField(upload_to="shopThings/gifs/", default="shopThings/gifs/6152297562.jpg")
    money = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    arr_skins = models.ManyToManyField(Shop)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Rating(models.Model):
    rating = models.IntegerField(default=1000)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Raiting"
        verbose_name_plural = "Raitings"

