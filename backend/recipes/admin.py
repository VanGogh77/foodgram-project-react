from django.contrib import admin

from recipes.models import (Favorite, Ingredient,
                            IngredientAmount, Recipe,
                            ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    """Класс настройки тегов."""

    list_display = ('pk', 'name',
                    'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    """Класс настройки ингредиентов."""

    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientAmountInline(admin.TabularInline):
    """Класс добавления ингредиентов."""

    model = IngredientAmount
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    """Класс настройки рецептов."""

    list_display = ('pk', 'name', 'author',
                    'text', 'get_tags', 'get_ingredients',
                    'cooking_time', 'image', 'pub_date',
                    'count_favorite')
    inlines = [IngredientAmountInline, ]
    search_fields = ('author', 'name')
    list_editable = ('author',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def get_ingredients(self, object):
        return '\n'.join(
            (ingredient.name for ingredient in object.ingredients.all())
        )
    get_ingredients.short_description = 'Ингредиенты'

    def get_tags(self, object):
        return '\n'.join((tag.name for tag in object.tags.all()))
    get_tags.short_description = 'Теги'

    def count_favorite(self, object):
        return object.favoriting.count()
    count_favorite.short_description = 'Избранное'


class IngredientAmountAdmin(admin.ModelAdmin):
    """Класс соответствия игредиентов и рецептов."""

    list_display = ('pk', 'ingredient',
                    'amount', 'recipe')
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    """Класс настройки избранного."""

    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    """Класс настройки списока покупок."""

    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user',)
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
