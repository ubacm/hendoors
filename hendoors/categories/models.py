from django.db import models
from django.urls import reverse

from hendoors.events.models import Event


class Category(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, models.CASCADE)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='categories')
    voting_open = models.NullBooleanField(help_text="Uses the event's default if not explicitly specified.")
    marks_required = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'pk': self.pk})

    def is_accepting_votes(self):
        return self.event.voting_open if self.voting_open is None else self.voting_open
