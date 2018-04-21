from django.urls import path

from . import views


app_name = 'categories'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='list'),
    path('<int:pk>/', views.CategoryDetailView.as_view(), name='detail'),
]
