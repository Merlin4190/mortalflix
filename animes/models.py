from django.db import models
from django.shortcuts import reverse

# Create your models here.
CATEGORY = (
    ('J', 'Japanese'),
    # ('G', 'Gollywood'),
    ('H', 'Hollywood'),
    # ('N', 'Nollywood')
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

  # def cat(self):
  #   return self.title

  class Meta:
    """docstring for Meta"""
    ordering = ['-created_on']

  def __str__(self):
    return self.title

  # def get_absolute_url(self):
  #   return reverse('category:category_detail', args=[self.slug])

class Anime(models.Model):
  title= models.CharField(max_length=200, unique=True)
  slug= models.SlugField(max_length=200, unique=True)
  category = models.CharField(choices=CATEGORY, max_length=2)
  # genre = models.CharField(max_length=200, default="", blank=True)
  runtime = models.CharField(max_length=200, default="", blank=True)
  label = models.CharField(choices=LABEL, max_length=2)
  description = models.TextField()
  avatar = models.ImageField(upload_to='images/avatar', default=None)
  adlink= models.URLField(max_length=200, default="", blank=True)
  created_on= models.DateTimeField(auto_now_add=True)
  updated_on= models.DateTimeField(auto_now=True)

  genres = models.ManyToManyField(Genre, related_name='series')


  class Meta:
    """docstring for Meta"""
    ordering = ['-created_on']

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('animes:seasons', kwargs={"slug" : self.slug})
  
  @property
  def no_of_comments(self):
    return Comment.objects.filter(anime=self).count()

class Season(models.Model) :
  anime = models.ForeignKey(Anime, default="", on_delete=models.CASCADE)
  title= models.CharField(max_length=200, unique=True)
  slug= models.SlugField(max_length=200, unique=True)
  # slug = AutoSlugField(populate_from='title', unique_with='created_on')
  tag = models.CharField(choices=TAG, max_length=2)
  adlink= models.URLField(max_length=200, default="", blank=True)
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("animes:episodes", kwargs={
        "slug" : self.slug
    
    })
  
  @property
  def no_of_comments(self):
    return Comment.objects.filter(season=self).count()

class Episode(models.Model) :
  anime = models.ForeignKey(Anime, default="", on_delete=models.CASCADE)
  season = models.ForeignKey(Season, on_delete=models.CASCADE)
  title= models.CharField(max_length=200, unique=True)
  description = models.TextField(default="", blank=True)
  slug= models.SlugField(max_length=200, unique=True)
  tag = models.CharField(choices=TAG, max_length=2)
  adlink= models.URLField(max_length=200, default="", blank=True)
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("animes:episode", kwargs={
        "slug" : self.slug
    
    })
  
  @property
  def no_of_comments(self):
    return Comment.objects.filter(episode=self).count()

class Download(models.Model) :
  anime = models.ForeignKey(Anime, default="", on_delete=models.CASCADE)
  season = models.ForeignKey(Season, on_delete=models.CASCADE)
  episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
  title= models.CharField(max_length=200, unique=True)
  link= models.URLField(max_length=200, unique=True)
  mediaformat= models.CharField(choices=FORMAT, max_length=3)
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.title
'''
class Cast(models.Model):
  anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='casts')
  name= models.CharField(max_length=200)
  imagelink = models.URLField(max_length=200, default="", blank=True)
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.name
'''    
class Comment(models.Model) :
  anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
  season = models.ForeignKey(Season, on_delete=models.CASCADE)
  episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
  name= models.CharField(max_length=200)
  email= models.EmailField(max_length=200)
  phone= models.CharField(max_length=200)
  content = models.TextField()
  created_on= models.DateTimeField(auto_now_add=True, null=True)
  updated_on= models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
    return self.name