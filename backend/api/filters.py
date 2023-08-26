from django_filters.rest_framework import FilterSet, filters
from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class RecipesFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited', method='filter_nonmodel_fields')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_nonmodel_fields')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class IngredientsFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
