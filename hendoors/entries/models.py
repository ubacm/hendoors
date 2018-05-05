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
    team = models.CharField(
        max_length=200, blank=True,
        help_text='Comma-separated list of email addresses.')

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if isinstance(self.team, str):
            self.team_list = self.team
        return super().save(*args, **kwargs)

    @property
    def team_list(self):
        return self.team.split(', ')

    @team_list.setter
    def team_list(self, emails):
        if not isinstance(emails, str):
            raise ValueError('Assignment to Entry.team_list requires a string')
        email_gen = (email.strip() for email in emails.split(','))
        self.team = ', '.join(sorted(filter(None, email_gen)))

    def get_absolute_url(self):
        return reverse('entries:detail', kwargs={'pk': self.pk})

    def can_be_edited_by(self, user):
        return (user.has_perm('entries.change_entry')
                or user.email in self.team_list)


class EntryImage(models.Model):
    entry = models.ForeignKey(Entry, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='entries')

    class Meta:
        verbose_name_plural = 'entry images'
