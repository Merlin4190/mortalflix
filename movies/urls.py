from django.urls import path
from . import views 
from .views import (
    HomeView,
    MovieView,
    SearchView
)
app_name = 'movies' 
urlpatterns = [
    path('', HomeView.as_view(), name='movies'),
    path('download/<slug>/', MovieView.as_view(), name='movie'),
    path('search/', SearchView.as_view(), name='search'),
    path('genre/<slug:slug>/', views.genre_list, name='genre_list'),
    path("alphasearch/", views.search_abc_list, name='searchlist'),
]