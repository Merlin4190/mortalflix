from django.urls import path
from . import views 
from .views import (
    HomeView,
    AnimeView,
    SeasonView,
    EpisodeView,
    SearchView
)
app_name = 'animes' 
urlpatterns = [
    path('', HomeView.as_view(), name='series'),
    path('seasons/<slug>/', AnimeView.as_view(), name='seasons'),
    path('episodes/<slug>/', SeasonView.as_view(), name='episodes'),
    path('download/<slug>/', EpisodeView.as_view(), name='episode'),
    path('search/', SearchView.as_view(), name='search'),
    path('genre/<slug:slug>/', views.genre_list, name='genre_list'),
    path("alphasearch/", views.search_abc_list, name='searchlist'),
]