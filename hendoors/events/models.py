from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    time = models.DateTimeField()
    voting_open = models.BooleanField(default=False)
