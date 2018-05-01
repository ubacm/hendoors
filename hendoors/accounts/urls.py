from django.contrib.auth import views as django_views
from django.urls import path


app_name = 'accounts'
urlpatterns = [
    path('logout/', django_views.LogoutView.as_view(), name='log-out'),
]
