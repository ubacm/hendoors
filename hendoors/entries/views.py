from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, UpdateView

from . import forms
from . import models


class _EntryTeammateRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        entry = self.get_entry()
        if not isinstance(entry, models.Entry):
            raise ValueError('{}.get_entry() must return an Entry object'
                             .format(self.__class__.__name__))
        has_access = entry.can_be_edited_by(self.request.user)
        if not has_access:
            messages.error(self.request, 'You do not have access to edit this entry.')
        return has_access


class _EntryFormViewMixin:
    model = models.Entry
    form_class = forms.EntryForm


class EntryCreateView(UserPassesTestMixin, _EntryFormViewMixin, CreateView):

    def get_initial(self):
        initial = super().get_initial()
        initial['team'] = self.request.user.email
        return initial

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_active


class EntryDetailView(DetailView):
    model = models.Entry


class EntryUpdateView(_EntryTeammateRequiredMixin, _EntryFormViewMixin, UpdateView):
    def get_entry(self):
        return self.get_object()


class EntryImageFormView(_EntryTeammateRequiredMixin, FormView):
    form_class = forms.EntryImageForm
    template_name = 'entries/entryimage_form.html'

    def get_entry(self):
        return models.Entry.objects.get(pk=self.kwargs['entry_pk'])

    def form_valid(self, form):
        images = self.request.FILES.getlist('images')
        for image in images:
            models.EntryImage.objects.create(
                entry_id=self.kwargs['entry_pk'],
                image=image,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('entries:detail', kwargs={'pk': self.kwargs['entry_pk']})
