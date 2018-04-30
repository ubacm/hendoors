from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, TemplateView

from hendoors.categories.models import Category
from hendoors.entries.models import Entry

from .forms import VoteCastForm
from .models import Vote


class VoteCastView(LoginRequiredMixin, FormView):
    form_class = VoteCastForm
    template_name = 'votes/vote_cast.html'

    def get_form(self, form_class=None):
        super().get_form(form_class=form_class)
        form = super().get_form(form_class=form_class)
        form.user = self.request.user
        return form

    def form_valid(self, form):
        category = form.cleaned_data['category']
        entry = form.cleaned_data['entry']
        weight = form.cleaned_data['weight']

        vote, created = Vote.objects.get_or_create(
            user=self.request.user,
            category=category,
            entry=entry,
            defaults={'weight': weight},
        )
        if not created:
            vote.weight = weight
            vote.save()

        return JsonResponse({'success': True})

    def form_invalid(self, form):
        all_errors = []
        for field, errors in form.errors.items():
            all_errors.extend(errors)
        return JsonResponse({
            'success': False,
            'errors': all_errors,
        })


class CategoryVoteStatisticsView(TemplateView):
    template_name = 'votes/category_vote_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = get_object_or_404(Category, id=context['category_id'])
        entries = (
            Entry.objects
            .filter(vote__category=category)
            .annotate(
                total=Coalesce(Sum('vote__weight'), 0)
            )
            .order_by('-total')
        )

        context.update({
            'category': category,
            'entries': entries,
        })
        return context


class EntryVoteStatisticsView(TemplateView):
    template_name = 'votes/entry_vote_statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entry = get_object_or_404(Entry, id=context['entry_id'])
        categories = (
            Category.objects
            .filter(vote__entry=entry)
            .annotate(
                total=Coalesce(Sum('vote__weight'), 0)
            )
            .order_by('-total')
        )

        context.update({
            'categories': categories,
            'entry': entry,
        })
        return context
