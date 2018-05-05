from django.views.generic import DetailView, ListView

from hendoors.entries.models import Entry
from .models import Category


class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entry_voted_for'] = Entry.objects.filter(
            vote__category=self.object,
            vote__user=self.request.user,
        ).first()
        return context


class CategoryListView(ListView):
    model = Category
