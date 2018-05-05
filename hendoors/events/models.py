from django.db import models
from django.urls import reverse


class Event(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(
        max_length=10, blank=True,
        help_text='The check-in code for the event; not currently used.')
    description = models.TextField()
    location = models.CharField(max_length=50)
    time = models.DateTimeField()
    is_accepting_votes = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})
