# Generated by Django 3.2.3 on 2023-08-09 10:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('units', models.CharField(max_length=150, verbose_name='Еденицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=150, unique=True, verbose_name=users.models.User)),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(unique=True, verbose_name='Время приготовления в минутах')),
                ('ingredients', models.ManyToManyField(to='recipes.Ingredient', verbose_name='Ингредиенты')),
            ],
            options={
                'verbose_name': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('color', models.CharField(max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator('^#([a-fA-F0-9]{6})', message='Поле HEX-кода выбираемого цвета.')], verbose_name='Цвет')),
                ('slug', models.SlugField(max_length=150, null=True, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Тег',
            },
        ),
        migrations.CreateModel(
            name='Shopping_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipes', verbose_name='Рецепт в списке покупок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список покупок',
            },
        ),
        migrations.AddField(
            model_name='recipes',
            name='tag',
            field=models.ManyToManyField(to='recipes.Tag', verbose_name='Тег'),
        ),
        migrations.CreateModel(
            name='Recipe_page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipes', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Ингредиенты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipes', verbose_name='Избранный рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
            },
        ),
        migrations.AddConstraint(
            model_name='shopping_list',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_list'),
        ),
        migrations.AddConstraint(
            model_name='recipe_page',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_combination'),
        ),
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorites'),
        ),
    ]
