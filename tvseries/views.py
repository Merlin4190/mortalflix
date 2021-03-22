import string
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView, DetailView
from .models import (                           
    Series,
    Season,
    Episode,
    Download,
    Cast,
    Genre,
    Comment
)

alphabet = string.ascii_uppercase

# Create your views here.
class HomeView(ListView):
    model = Series
    context_object_name = 'series'
    template_name = "tvseries.html"
    extra_context={'alphabet': alphabet}
    ordering = ['created_on']
    # queryset = Series.objects.order_by('created_on')[:6]
    paginate_by = 6

    def get_context_data(self,*args, **kwargs): 
        context = super(HomeView, self).get_context_data(*args,**kwargs) 
        context['episodes']= Episode.objects.order_by('-created_on')[:10]

        list_series = Series.objects.all()
        paginator = Paginator(list_series, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_series = paginator.page(page)
        except PageNotAnInteger:
            file_series = paginator.page(1)
        except EmptyPage:
            file_series = paginator.page(paginator.num_pages)
            
        context['list_series'] = file_series

        return context

class SeriesView(DetailView):
    Model = Series
    context_object_name = 'seasons'
    template_name = "season_lists.html"
    queryset = Series.objects.all()

    def get_context_data(self, **kwargs):
        self.series = get_object_or_404(Series, slug=self.kwargs['slug'])
        context = super(SeriesView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        seasons = paginator = Paginator(Season.objects.filter(series=self.series).order_by('created_on'), 10)
        context['seasons'] = seasons.get_page(page)
        context['series'] = Series.objects.all()
        return context

class SeasonView(DetailView):
    context_object_name = 'episodes'
    template_name = "episode_lists.html"
    queryset = Season.objects.all()

    def get_context_data(self, **kwargs):
        self.season = get_object_or_404(Season, slug=self.kwargs['slug'])
        context = super(SeasonView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        episodes = paginator = Paginator(Episode.objects.filter(season=self.season).order_by('created_on'), 10)
        context['episodes'] = episodes.get_page(page)
        return context

class EpisodeView(DetailView):
    context_object_name = 'episode'
    template_name = "download.html"
    queryset = Episode.objects.all()

    def get_context_data(self, **kwargs):
        self.episode = get_object_or_404(Episode, slug=self.kwargs['slug'])
        context = super(EpisodeView, self).get_context_data(**kwargs)
        context['episode'] = Download.objects.filter(episode=self.episode)
        context['comments'] = Comment.objects.filter(episode=self.episode).order_by('-created_on')

        return context
    
    def post(self, request, *args,**kwargs):
        self.episode = get_object_or_404(Episode, slug=self.kwargs['slug'])
        new_comment = Comment(content=request.POST.get('content'),
                            name = request.POST.get('name'),
                            email = request.POST.get('email'),
                            phone = request.POST.get('phone'),
                            episode = self.get_object(),
                            season = Season.objects.get(episode=self.episode),
                            series = Series.objects.get(episode=self.episode)
        )
        new_comment.save()
        return self.get(self, request, *args, **kwargs)

class SearchView(ListView):
    model = Series
    template_name = "search_series.html"
    extra_context={'alphabet': alphabet}

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        
        if query is not None:
            lookups= Q(title__icontains=query) & Q(category__icontains=filter_field)

            results= Series.objects.filter(lookups).distinct()

            return results

        else:
            return Series.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = {
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', '')
        }

        return context

def genre_list(request, slug):
  series = Series.objects.filter(
      genres__slug__contains=slug
  ).order_by('-created_on').distinct()

  genres = Genre.objects.all()
  genre_row = Genre.objects.filter(slug=slug)

  context = {'slug': slug, 'gen': genre_row, 'series': series, 'genres': genres }
  return render(request, 'genre.html', context)

def search_abc_list(request):
    series = Series.objects.all()
    # context_object_name = 'searchlist'
    
    if request.method == 'GET':
        query= request.GET.get('list')

        if query is not None:

            if query in alphabet.upper():
                lookups= Q(title__startswith=query)

                results= Series.objects.filter(lookups).distinct()

                context={'results': results, 'series': series, 'alphabet': alphabet}

                return render(request, 'series_abc_list.html', context)

            else:
                
                lookups= Q(title__regex =r'^\d[\w\d _-]+')
                # lookups= Q(title__startswith = 2)

                results= Series.objects.filter(lookups).distinct()

                context={'results': results, 'series': series}

                return render(request, 'series_abc_list.html', context)

        else:
            return render(request, 'series_abc_list.html')

    else:
        return render(request, 'series_abc_list.html')