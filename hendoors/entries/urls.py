from django.urls import path

from . import views


app_name = 'entries'

urlpatterns = [
    path('<int:pk>/', views.EntryDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EntryUpdateView.as_view(), name='update'),
    path('<int:entry_pk>/images/', views.EntryImageFormView.as_view(), name='upload-images'),
    path('new/', views.EntryCreateView.as_view(), name='create'),
]
