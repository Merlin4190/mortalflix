import string
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView, DetailView
from .models import (                           
    Movie,
    Download,
    Cast,
    Genre,
    Comment
)

alphabet = string.ascii_uppercase

# Create your views here.
class HomeView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = "movies.html"
    extra_context={'alphabet': alphabet}
    ordering = ['created_on']
    paginate_by = 6

    def get_context_data(self,*args, **kwargs): 
        context = super(HomeView, self).get_context_data(*args,**kwargs) 
        context['movies']= Movie.objects.order_by('-year')[:10]

        list_movies = Movie.objects.all()
        paginator = Paginator(list_movies, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_movies = paginator.page(page)
        except PageNotAnInteger:
            file_movies = paginator.page(1)
        except EmptyPage:
            file_movies = paginator.page(paginator.num_pages)
            
        context['list_series'] = file_movies

        return context

class MovieView(DetailView):
    model = Movie
    context_object_name = 'movie'
    template_name = "movie-details.html"
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        self.movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
        context = super(MovieView, self).get_context_data(**kwargs)
        context['downloads'] = Download.objects.filter(movie=self.movie)
        context['comments'] = Comment.objects.filter(movie=self.movie).order_by('-created_on')

        return context

    def post(self, request, *args,**kwargs):
        self.movie = get_object_or_404(Movie, slug=self.kwargs['slug'])
        new_comment = Comment(content=request.POST.get('content'),
                            name = request.POST.get('name'),
                            email = request.POST.get('email'),
                            phone = request.POST.get('phone'),
                            movie = self.get_object()
        )
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class SearchView(ListView):
    model = Movie
    template_name = "search_series.html"
    extra_context={'alphabet': alphabet}

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        
        if query is not None:
            lookups= Q(title__icontains=query) & Q(category__icontains=filter_field)

            results= Movie.objects.filter(lookups).distinct()

            return results

        else:
            return Movie.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = {
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', '')
        }

        return context

def genre_list(request, slug):
  movies = Movie.objects.filter(
      genres__slug__contains=slug
  ).order_by('-year').distinct()

  genres = Genre.objects.all()
  genre_row = Genre.objects.filter(slug=slug)

  context = {'slug': slug, 'gen': genre_row, 'movies': movies, 'genres': genres }
  return render(request, 'movie_genre.html', context)

def search_abc_list(request):
    movies = Movie.objects.all()
    
    if request.method == 'GET':
        query= request.GET.get('list')

        if query is not None:

            if query in alphabet.upper():
                lookups= Q(title__startswith=query)

                results= Movie.objects.filter(lookups).distinct()

                context={'results': results, 'movies': movies, 'alphabet': alphabet}

                return render(request, 'movies_abc_list.html', context)

            else:
                
                lookups= Q(title__regex =r'^\d[\w\d _-]+')
                # lookups= Q(title__startswith = 2)

                results= Movie.objects.filter(lookups).distinct()

                context={'results': results, 'movies': movies}

                return render(request, 'movies_abc_list.html', context)

        else:
            return render(request, 'movies_abc_list.html')

    else:
        return render(request, 'movies_abc_list.html')