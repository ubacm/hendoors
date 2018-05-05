import os
import uuid

from django.db import models
from django.urls import reverse

from hendoors.categories.models import Category


class Entry(models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category, related_name='entries')
    description = models.TextField()
    team = models.CharField(
        max_length=200, blank=True,
        help_text='Comma-separated list of email addresses.')
    website = models.URLField(blank=True)
    repository = models.URLField(blank=True)

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
        if not user.is_authenticated or not user.is_active:
            return False
        return (user.has_perm('entries.change_entry')
                or user.email in self.team_list)


def _generate_file_path(instance, old_file_name):
    extension = os.path.splitext(old_file_name)[1]
    new_file_name = '{}{}'.format(
        ''.join(str(uuid.uuid4()).split('-')),
        extension,
    )
    file_path = os.path.join('entries', str(instance.entry_id), new_file_name)
    return file_path


class EntryImage(models.Model):
    entry = models.ForeignKey(Entry, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=_generate_file_path)

    class Meta:
        verbose_name_plural = 'entry images'
