from django.contrib import admin
from .models import Series, Season, Episode, Download, Cast, Genre, Trailer

# Register your models here.
class CastAdmin(admin.ModelAdmin):
  pass

class CastInline(admin.StackedInline):
  model = Cast
  max_num = 5
  extra = 0

class SeriesAdmin(admin.ModelAdmin):

#   list_display = ('title', 'slug', 'status', 'created_on')
#   list_filter = ('status',)
  search_fields = ['title', 'content']
  prepopulated_fields = {'slug':('title',)}
  inlines = [CastInline,]

class SeasonAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('title',)}

class EpisodeAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('title',)}

class GenreAdmin(admin.ModelAdmin):
  # list_display = ('title', 'slug', 'created_on')
  search_fields = ['title',]
  prepopulated_fields = {'slug':('title',)}

admin.site.register(Genre, GenreAdmin)
admin.site.register(Cast, CastAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Trailer)
admin.site.register(Download)
