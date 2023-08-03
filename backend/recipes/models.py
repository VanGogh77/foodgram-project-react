from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=150,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=15,
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле HEX-кода выбираемого цвета.'

            )
        ]
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=150,
        unique=True,
        null=True
    )

    class Meta:
        verbose_name = 'Тег'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.CharField(
        verbose_name='Автор',
        max_length=150,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=150,
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
    )


class Shopping_list(models.Model):


class Favorites(models.Model):


class Ingredient(models.Model):

