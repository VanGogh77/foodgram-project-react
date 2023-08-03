from django_filters import rest_framework

from recipes.models import Recipes


class RecipesFilter(rest_framework.FilterSet):
    tag = rest_framework.CharFilter(
        field_name='tag', lookup_expr='icontains'
    )

    class Meta:
        model = Recipes
        fields = 'tag'