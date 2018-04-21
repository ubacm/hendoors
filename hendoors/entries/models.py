from django.db import models

from hendoors.categories.models import Category


class Entry(models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    description = models.TextField()
    website = models.URLField(blank=True)
    repository = models.URLField(blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.name


class EntryImage(models.Model):
    entry = models.ForeignKey(Entry, models.CASCADE, related_name='images')

    class Meta:
        verbose_name_plural = 'entry images'
