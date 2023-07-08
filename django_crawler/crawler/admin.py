from django.contrib import admin

from django.contrib import admin
from .models import Movie, History

class MovieAdmin(admin.ModelAdmin):
    pass


class HistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Movie, MovieAdmin)
admin.site.register(History, HistoryAdmin)
