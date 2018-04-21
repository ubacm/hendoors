from django.db import models
from django.urls import reverse


class Event(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    description = models.TextField()
    location = models.CharField(max_length=50)
    time = models.DateTimeField()
    voting_open = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
