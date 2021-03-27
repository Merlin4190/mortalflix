import string
from django.apps import apps
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView, DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, auth
from django.contrib import messages
from tvseries.models import Series, Trailer as STrailer
from animes.models import Anime, Trailer as ATrailer
from movies.models import Movie, Trailer as MTrailer

alphabet = string.ascii_uppercase

# Create your views here.
class HomeView(ListView):
    model = Movie
    context_object_name = 'movies'
    template_name = "home.html"
    extra_context={'alphabet': alphabet}
    ordering = ['year']
    paginate_by = 6

    def get_context_data(self,*args, **kwargs): 
        context = super(HomeView, self).get_context_data(*args,**kwargs) 
        context['animes']= Anime.objects.order_by('-created_on')[:10]
        context['series']= Series.objects.order_by('-created_on')[:10]
        context['mtrailers']= MTrailer.objects.order_by('-created_on')[:1]
        context['atrailers']= ATrailer.objects.order_by('-created_on')[:1]
        context['strailers']= STrailer.objects.order_by('-created_on')[:1]

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

class RegisterView(View):
    def get(self, request):
        return render(request, 'home.html')
    
    def post(self, request):
        uname = request.POST['username']
        # fname = request.POST['fname']
        # lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password_length = len(password)

        if password_length > 8:

            if User.objects.filter(username=uname).exists():
                messages.info(request, 'Username already exist', extra_tags='register')
                return redirect('myflix:home')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exist', extra_tags='register')
                return redirect('myflix:home')
            else:
                user = User.objects.create_user(username=uname, password=password, email=email)
                user.save()
                messages.info(request, 'User created', extra_tags='register')
                return redirect(reverse('myflix:home'))
        else:
            messages.info(request, 'password length is too small', extra_tags='register')
            return redirect('myflix:home')
        # return redirect('/')

        return render(request, 'home.html')

        # if form.is_valid():
        #     user = form.save()
        #     return redirect(reverse('login'))
        # return render(request, 'home.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'home.html')
    
    def post(self, request):
        uname = request.POST['username']
        # email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=uname, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('myflix:home'))
        else:
            messages.info(request, 'Wrong username or password', extra_tags='login')
            return redirect('myflix:home')

        return render(request, "home.html")

class ProfileView(LoginRequiredMixin, UpdateView):
    
    model = User
    login_url ='/'
    success_url = reverse_lazy('myflix:home')
    template_name = 'profile.html'

    def get(self, request, pk):
        return render(request, 'profile.html')
    
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        user.firstname = request.POST['fname']
        user.lastname = request.POST['lname']
        # email = request.POST['email']
        user.profile.phone = request.POST['phone']
        user.profile.bio = request.POST['bio']
        # user = User.objects.update_user(firstname=fname, lastname=lname, phone=phone, bio=bio)
        user.save()
        messages.info(request, 'Profile Updated', extra_tags='profile')

        return render(request, 'profile.html')

class SearchView(ListView):
    model = Series
    template_name = "search_series.html"
    extra_context={'alphabet': alphabet}

    def get_queryset(self):
        query = self.request.GET.get('search')
        Cat = self.request.GET.get('filter_field')
        if Cat == 'Series':

            Model = apps.get_model('tvseries', 'Series')

            if query is not None:
                lookups= Q(title__icontains=query)

                results= Model.objects.filter(lookups).distinct()

                return results

            else:
                return Model.objects.all()
                
        elif Cat == 'Anime':

            Model = apps.get_model('animes', 'Anime')

            if query is not None:
                lookups= Q(title__icontains=query)

                results= Model.objects.filter(lookups).distinct()

                # context={'results': results}

                return results

            else:
                return Model.objects.all()

        elif Cat == 'Movie':

            Model = apps.get_model('movies', 'Movie')

            if query is not None:
                lookups= Q(title__icontains=query)

                results= Model.objects.filter(lookups).distinct()

                # context={'results': results}

                return results

            else:
                return Model.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = {
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', '')
        }

        return context

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
                
                lookups= Q(title__regex =r'^[a-zA-Z].*$')
                # lookups= Q(title__startswith = 2)

                results= Series.objects.filter(lookups).distinct()

                context={'results': results, 'series': series}

                return render(request, 'series_abc_list.html', context)

        else:
            return render(request, 'series_abc_list.html')

    else:
        return render(request, 'series_abc_list.html')
