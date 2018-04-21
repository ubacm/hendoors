from django.views.generic import DetailView, ListView

from .models import Category


class CategoryDetailView(DetailView):
    model = Category


class CategoryListView(ListView):
    model = Category
