from django.db import models
from django.shortcuts import reverse

# Create your models here.
CATEGORY = (
    ('B', 'Bollywood'),
    ('C', 'Chinese'),
    ('F', 'French'),
    ('G', 'German'),
    ('Go', 'Gollywood'),
    ('H', 'Hollywood'),
    ('J', 'Japanese'),
    ('K', 'Korean'),
    ('N', 'Nollywood'),
    ('S', 'Spanish')
)

LABEL = (
    ('L', 'Latest'),
    ('R', 'Recently Released'),
    ('S', 'Coming Soon'),
    ('T', 'Top Rated'),
)

TAG = (
    ('N', 'New'),
    ('SP', 'Season Priemere'),
    ('SF', 'Season Finale'),
)

FORMAT = (
    ('MP4', 'Mp4'),
    ('3GP', '3gp'),
    ('HD', 'High Definition'),
)

class Genre(models.Model):
  title= models.CharField(max_length=200, unique=True)
  slug= models.SlugField(max_length=200, unique=True)
  created_on= models.DateTimeField(auto_now_add=True)
  updated_on= models.DateTimeField(auto_now=True)

  class Meta:
    """docstring for Meta"""
    ordering = ['-created_on']

  def __str__(self):
    return self.title

  # def get_absolute_url(self):
  #   return reverse('category:category_detail', args=[self.slug])

class Movie(models.Model):
  title= models.CharField(max_length=200, unique=True)
  slug= models.SlugField(max_length=200, unique=True)
  category = models.CharField(choices=CATEGORY, max_length=2)
  year = models.CharField(max_length=200, default="", blank=True)
  writer = models.CharField(max_length=200, default="", blank=True)
  director = models.CharField(max_length=200, default="", blank=True)
  language = models.CharField(max_length=200, default="", blank=True)
  runtime = models.CharField(max_length=200, default="", blank=True)
  label = models.CharField(choices=LABEL, max_length=2)
  description = models.TextField()
  avatar = models.ImageField(upload_to='images/avatar', default=None)
  adlink= models.URLField(max_length=200, default="", blank=True)
  created_on= models.DateTimeField(auto_now_add=True)
  updated_on= models.DateTimeField(auto_now=True)

  genres = models.ManyToManyField(Genre, related_name='movies')


  class Meta:
    """docstring for Meta"""
    ordering = ['-created_on']

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('movies:movie', kwargs={"slug" : self.slug})
  
  @property
  def no_of_comments(self):
    return Comment.objects.filter(movie=self).count()


class Download(models.Model) :
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='downloads')
  title= models.CharField(max_length=200, unique=True)
  link= models.URLField(max_length=200, unique=True)
  mediaformat= models.CharField(choices=FORMAT, max_length=3)
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.title

class Cast(models.Model):
  Movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='casts')
  name= models.CharField(max_length=200)
  imagelink = models.URLField(max_length=200, default="", blank=True)
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.name

class Trailer(models.Model):
  title= models.CharField(max_length=200)
  imagelink = models.URLField(max_length=200, default="", blank=True)
  link= models.URLField(max_length=200, unique=True)
  release_date= models.DateField(null=True)
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.title

class Comment(models.Model) :
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
  name= models.CharField(max_length=200)
  email= models.EmailField(max_length=200)
  phone= models.CharField(max_length=200)
  content = models.TextField()
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.name