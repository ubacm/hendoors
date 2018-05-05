from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Entry


class _EntryFormViewMixin(LoginRequiredMixin):
    model = Entry
    fields = ('name', 'categories', 'description', 'team', 'website', 'repository')


class EntryCreateView(_EntryFormViewMixin, CreateView):
    def get_initial(self):
        initial = super().get_initial()
        initial['team'] = self.request.user.email
        return initial


class EntryDetailView(DetailView):
    model = Entry


class EntryUpdateView(_EntryFormViewMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        entry = self.get_object()
        user = self.request.user
        return entry.can_be_edited_by(user)
