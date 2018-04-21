from django.urls import path

from . import views


app_name = 'votes'

urlpatterns = [
    path('cast/', views.VoteCastView.as_view(), name='cast'),
    path('categories/<int:category_id>/', views.CategoryVoteStatisticsView.as_view(), name='categories'),
    path('entries/<int:entry_id>/', views.EntryVoteStatisticsView.as_view(), name='entries'),
]
