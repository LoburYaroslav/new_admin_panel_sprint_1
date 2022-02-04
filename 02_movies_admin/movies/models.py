import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'))
    birth_date = models.DateField(_('birth_date'), blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmWorkTypeChoices(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(_('creation_date'), blank=True, null=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(
        _('type'),
        max_length=7,
        choices=FilmWorkTypeChoices.choices,
        default=FilmWorkTypeChoices.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork', verbose_name=_('genres'), )
    persons = models.ManyToManyField(Person, through='PersonFilmWork', verbose_name=_('persons'))
    certificate = models.CharField(_('certificate'), max_length=512, blank=True, null=True)
    # Параметр upload_to указывает, в какой подпапке будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('film_work')
        verbose_name_plural = _('film_works')


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.RESTRICT)
    genre = models.ForeignKey('Genre', on_delete=models.RESTRICT, verbose_name=_('genre'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _('film_work_genre_rel')
        verbose_name_plural = _('film_work_genre_rel_plural')

        indexes = [
            models.Index(fields=['genre'], name='genre_film_work_genre_idx'),
            models.Index(fields=['film_work'], name='genre_film_work_film_work_idx'),
        ]

        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='unique_film_work_genre')
        ]


class PersonFilmWork(UUIDMixin):
    class PersonFilmWorkRoleChoices(models.TextChoices):
        DIRECTOR = 'director', _('director')
        WRITER = 'writer', _('writer')
        ACTOR = 'actor', _('actor')

    film_work = models.ForeignKey('FilmWork', on_delete=models.RESTRICT)
    person = models.ForeignKey('Person', on_delete=models.RESTRICT)
    role = models.CharField(
        _('role'),
        max_length=8,
        choices=PersonFilmWorkRoleChoices.choices,
        default=PersonFilmWorkRoleChoices.ACTOR,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _('person_film_work_rel_plural')
        verbose_name_plural = _('person_film_work_rel_plural')

        indexes = [
            models.Index(fields=['person'], name='person_film_work_person_idx'),
            models.Index(fields=['film_work'], name='person_film_work_film_work_idx'),
        ]

        constraints = [
            models.UniqueConstraint(fields=['person', 'film_work', 'role'], name='unique_film_work_member')
        ]
