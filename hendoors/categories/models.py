from django.db import models
from django.urls import reverse

from hendoors.events.models import Event


class Category(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, models.CASCADE)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='categories')
    marks_required = models.IntegerField(default=0)
    is_accepting_entries = models.BooleanField(default=False)
    is_accepting_votes = models.NullBooleanField(
        help_text="Uses the event's default if not explicitly specified.")

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'pk': self.pk})

    @property
    def can_accept_votes(self):
        if self.is_accepting_votes is not None:
            return self.is_accepting_votes
        return self.event.is_accepting_votes
