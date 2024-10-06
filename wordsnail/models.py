from django.db import models

class Raiting(models.Model):
    user_id = models.IntegerField()
    raiting = models.IntegerField()
    count = models.IntegerField()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Raiting"
        verbose_name_plural = "Raitings"
