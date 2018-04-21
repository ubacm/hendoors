from django.urls import path

from . import views


app_name = 'entries'

urlpatterns = [
    path('<int:pk>/', views.EntryDetailView.as_view(), name='detail'),
]