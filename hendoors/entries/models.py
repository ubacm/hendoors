from django.conf import settings
from django.db import models
from django.urls import reverse

from hendoors.categories.models import Category


class Entry(models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category, related_name='entries')
    description = models.TextField()
    website = models.URLField(blank=True)
    repository = models.URLField(blank=True)
    team = models.ManyToManyField(settings.AUTH_USER_MODEL, 'entries')

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('entries:detail', kwargs={'pk': self.pk})


class EntryImage(models.Model):
    entry = models.ForeignKey(Entry, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='entries')

    class Meta:
        verbose_name_plural = 'entry images'
