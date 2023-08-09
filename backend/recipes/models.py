from django.db import models
from django.core.validators import RegexValidator

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


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=150,
        unique=True,
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
    )
    units = models.CharField(
        verbose_name='Еденицы измерения',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.units}'
    

class Recipes(models.Model):
    author = models.CharField(
        User,
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
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        unique=True,
    )

    class Meta:
        verbose_name = 'Рецепты'

    def __str__(self):
        return self.name


class Recipe_page(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_combination',
            )
        ]

    def __str__(self):
        return (f'{self.recipe.name}: '
               f'{self.ingredient.name} - '
               f'{self.ingredient.quantity} '
               f'{self.ingredient.units}')


class Shopping_list(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт в списке покупок'
    )

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_list',
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorites',
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
