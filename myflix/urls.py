from django.contrib.auth import views as auth_views
# from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views 
from .views import (
    HomeView,
    SearchView,
    RegisterView,
    ProfileView,
    LoginView
)
app_name = 'myflix' 
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path("alphasearch/", views.search_abc_list, name='searchlist'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]