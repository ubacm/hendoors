from django.contrib import admin

from . import models


@admin.register(models.Vote)
class VoteModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'entry', 'weight')
    list_display_links = ('weight',)
