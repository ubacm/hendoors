from django.urls import path

from . import views


app_name = 'votes'

urlpatterns = [
    path('cast/', views.VoteCastView.as_view(), name='cast'),
]
