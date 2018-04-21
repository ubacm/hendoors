from django.views.generic import DetailView

from .models import Entry


class EntryDetailView(DetailView):
    model = Entry
