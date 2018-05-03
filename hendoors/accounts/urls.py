from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.LogInView.as_view(), name='log-in'),
    path('login/slack/', views.SlackLogInView.as_view(), name='slack-log-in'),
    path('logout/', views.LogOutView.as_view(), name='log-out'),
]
