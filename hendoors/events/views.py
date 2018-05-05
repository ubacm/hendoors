from django.views.generic import DetailView, ListView

from .models import Event


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_categories_accepting_entries'] = (
            self.object.category_set.filter(is_accepting_entries=True).exists())
        return context


class EventListView(ListView):
    model = Event
