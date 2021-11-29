from django.db import models

from .utils import from_cyrillic_to_eng


class City(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Name City',
        unique=True
    )
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Name City'
        verbose_name_plural = 'Name City'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Язык программирования',
        unique=True
    )
    slug = models.TextField(blank=True, unique=True)

    class Meta:
        verbose_name = 'Name Language'
        verbose_name_plural = 'Names Language'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Вакансия')
    company = models.CharField(max_length=250)
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        verbose_name='city'
    )
    Language = models.ForeignKey(
        'Language',
        on_delete=models.CASCADE,
        verbose_name='language'
    )
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Name Vacancy'
        verbose_name_plural = 'Names Vacancy'

    def __str__(self) -> str:
        return self.title
