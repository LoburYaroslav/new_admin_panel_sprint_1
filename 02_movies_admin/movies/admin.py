from django.contrib import admin
from movies.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmWork
    raw_id_fields = ['genre']


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    raw_id_fields = ['person']


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)  # пока пофиксил долгие запросы с помощью raw_id_fields
    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
