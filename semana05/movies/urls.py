from django.urls import path
from movies.views import MovieRecommendationView

app_name = 'movies'

urlpatterns = [
    path('recommendations/', MovieRecommendationView.as_view(), name='recommendations'),
]