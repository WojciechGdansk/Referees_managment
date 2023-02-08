from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

from django.template.defaultfilters import slugify


# Create your models here.
class User(AbstractUser):
    phone_number = models.IntegerField(verbose_name="Numer telefonu", null=True)
    league = models.ForeignKey('League', on_delete=models.PROTECT, null=True)
    slug = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username + " " + str(int(datetime.datetime.now().timestamp())))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name + " " + self.last_name


class League(models.Model):
    which_league = models.CharField(max_length=100, verbose_name="Liga/klasa")
    slug = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.which_league + " " + str(int(datetime.datetime.now().timestamp())))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.which_league
