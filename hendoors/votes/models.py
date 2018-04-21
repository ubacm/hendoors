from django.conf import settings
from django.db import models

from hendoors.categories.models import Category
from hendoors.entries.models import Entry


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    category = models.ForeignKey(Category, models.CASCADE)
    entry = models.ForeignKey(Entry, models.CASCADE)
    weight = models.IntegerField(default=1)
