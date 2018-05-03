from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Entry


class _EntryFormViewMixin(LoginRequiredMixin):
    model = Entry
    fields = ('name', 'categories', 'description', 'website', 'repository')


class EntryCreateView(_EntryFormViewMixin, CreateView):
    pass


class EntryDetailView(DetailView):
    model = Entry


class EntryUpdateView(_EntryFormViewMixin, UpdateView):
    pass
