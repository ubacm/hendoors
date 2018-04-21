from django.views.generic import DetailView, ListView

from .models import Event


class EventDetailView(DetailView):
    model = Event


class EventListView(ListView):
    model = Event
