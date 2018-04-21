from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import VoteCastForm
from .models import Vote


class VoteCastView(FormView):
    form_class = VoteCastForm
    template_name = 'votes/vote_cast.html'

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

        return redirect(entry)
