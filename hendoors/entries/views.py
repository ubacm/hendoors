from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .models import Entry


class _EntryFormViewMixin(LoginRequiredMixin):
    model = Entry
    fields = ('name', 'categories', 'description', 'website', 'repository')


class EntryCreateView(_EntryFormViewMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.team.add(self.request.user)
        return response


class EntryDetailView(DetailView):
    model = Entry


class EntryUpdateView(_EntryFormViewMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        entry = self.get_object()
        user = self.request.user
        return entry.can_be_edited_by(user)
